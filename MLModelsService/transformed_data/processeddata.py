from typing import Dict, List, Tuple, Optional
import pandas as pd
from sqlalchemy import create_engine
import re
from datetime import datetime
from functools import lru_cache
import logging
from settings import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

query = '''
SELECT 
sales.order_id, sales.created, sales.state, sales.quantity, sales.price, sales.sum, sales.city, sales."shipmentAddress",
assortment.pathname, assortment.name AS assortment_name, assortment.volume,
agents.name AS agent_name, agents."companyType"
FROM sales
JOIN assortment on sales.assortment_id = assortment.id
JOIN agents on sales.agent_id = agents.agent_id
'''

engine = create_engine(settings.SQLALCHEMY_SYNC_DB_URL)

date_column = 'created'

class ProcessedData:
    """
    Singleton class for processing and storing sales data.
    Ensures only one instance exists across the application.
    """
    __instance: Optional['ProcessedData'] = None
    __initialized: bool = False

    def __new__(cls, *args, **kwargs) -> 'ProcessedData':
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, query: str = query, engine = engine, date_column: str = date_column):
        """Initialize ProcessedData if not already initialized."""
        if not ProcessedData.__initialized:
            try:
                logger.info("Initializing ProcessedData instance")
                self._initialize(query, engine, date_column)
                ProcessedData.__initialized = True
            except Exception as e:
                logger.error(f"Error initializing ProcessedData: {e}")
                raise

    def _initialize(self, query: str, engine, date_column: str) -> None:
        """Separate initialization logic for better control."""
        self._query = query
        self._engine = engine
        self._date_column = date_column
        
        # Initialize data
        self.update_data()
        
        # Initialize dictionaries for data access
        self.slice_dictionary: Dict[str, List[pd.DataFrame]] = {
            'today': [self.today_df, self.today_conv_df],
            'yesterday': [self.yesterday_df, self.yesterday_conv_df],
            'week': [self.week_df, self.week_conv_df],
            'month': [self.month_df, self.month_conv_df],
            'year': [self.year_df, self.year_conv_df],
            'all': [self.df, self.conv_df]
        }
        
        self.data_type_dict: Dict[str, int] = {
            'basic': 0,
            'conv': 1
        }

    @lru_cache(maxsize=32)
    def get_prepocessdata_slice(self, period: str = 'all', data_type: str = 'basic') -> pd.DataFrame:
        """Cached access to data slices."""
        return self.slice_dictionary[period][self.data_type_dict[data_type]]

    def update_data(self) -> None:
        """Update all data frames with fresh data from database."""
        try:
            logger.info("Starting data update")
            with self._engine.connect() as conn:
                raw_df = pd.read_sql(
                    sql=self._query,
                    con=conn.connection
                )
            if raw_df.empty:
                logger.error("No data was retrieved from the database. DataFrame is empty.")
                raise ValueError("The query returned an empty DataFrame.")
            
            logger.info(f"Successfully retrieved {len(raw_df)} rows from the database.")

            # raw_df = pd.read_sql(self._query, self._engine) stop working at pandas 2.2.0
            
            # Process main dataframe
            self.df = self.__get_final_df(raw_df, self._date_column)
            self.conv_df = self.__get_convolutional_table(self.df)
            
            # Update all time-based slices
            (self.today_df, self.yesterday_df, self.week_df, 
             self.month_df, self.year_df) = self.__get_dateslice_data(self.df, self._date_column)
            
            (self.today_conv_df, self.yesterday_conv_df, self.week_conv_df,
             self.month_conv_df, self.year_conv_df) = self.__get_dateslice_data(self.conv_df, self._date_column)
            
            # Clear the cache after update
            self.get_prepocessdata_slice.cache_clear()
            
            logger.info("Data update completed successfully")
        except Exception as e:
            logger.error(f"Error updating data: {e}")
            raise

    def __del__(self) -> None:
        """Cleanup when instance is deleted."""
        try:
            # Clear cache
            self.get_prepocessdata_slice.cache_clear()
            ProcessedData.__instance = None
            ProcessedData.__initialized = False
            logger.info("ProcessedData instance cleaned up")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

    @staticmethod
    def __get_final_df(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
        df = ProcessedData.__extract_volumes(df)
        df = ProcessedData.__add_dates_columns(df=df, date_column=date_column)
        df = ProcessedData.__extract_cities(df)
        df = ProcessedData.__add_path_columns(df)
        df = ProcessedData.__drop_some_irrelavant_data(df)
        
        df = df.reset_index(drop=True)

        return df

    #Group of methods that preproceess data
    @staticmethod
    def __extract_volumes(df: pd.DataFrame) -> pd.DataFrame:
        pattern = r'\b(\d+)\s*мл\b'
        df['volumes'] = df.assortment_name.str.extract(pattern, flags=re.IGNORECASE, expand=True)
        df.volumes = df.volumes.apply(lambda x: float(x))

        return df

    @staticmethod
    def __add_dates_columns(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
        date_dict = {
            'day': date_column + '_day',
            'dayofweek': date_column + '_dayofweek',
            'dayofweekname': date_column + '_dayofweekname',
            'week': date_column + '_week',
            'month': date_column + '_month',
            'year': date_column + '_year',
        }

        df.loc[:, date_dict['day']] = df[date_column].dt.date
        df.loc[:, date_dict['dayofweek']] = df[date_column].dt.dayofweek
        df.loc[:, date_dict['dayofweekname']] = df[date_column].dt.day_name()
        df.loc[:, date_dict['week']] = df[date_column].dt.isocalendar().week
        df.loc[:, date_dict['month']] = df[date_column].dt.month
        df.loc[:, date_dict['year']] = df[date_column].dt.year

        return df
    

    @staticmethod
    def __extract_cities(df: pd.DataFrame) -> pd.DataFrame:
        """
        Firsly this funstion try to find cities in more detailed address column and apply findings to city column
        After that make some data cleaning process
        """
        #first step
        cities = df.city.unique()
        pattern = re.compile('|'.join(cities))
        
        df['found_city'] = df['shipmentAddress'].apply(lambda x: pattern.search(x).group() if pattern.search(x) else 'Город не указан')
        df.city = df.apply(ProcessedData._compare_city, axis=1)
        
        #second step
        df.city = df.city.apply(lambda x: x.replace('г ', ''))

        return df

    @staticmethod
    def __add_path_columns(df: pd.DataFrame) -> pd.DataFrame:
        df_list = df.pathname.apply(lambda x: pd.Series(x.split('/'))).add_prefix('path_lvl_')
        df = df.join(df_list)
        return df

    @staticmethod
    def __drop_some_irrelavant_data(df: pd.DataFrame) -> pd.DataFrame:
        df = df[df.path_lvl_0 != 'Материалы']
        df = df[df.path_lvl_0 != 'Товары интернет-магазинов']
        df = df[df.state != 'Отменен']
        df.path_lvl_2 = df.apply(ProcessedData._compare_path_depth, axis=1)


        df = df[['order_id', 'created', 'agent_name', 'companyType', 'assortment_name', 'state', 
                'quantity', 'price', 'sum', 'city', 'volumes',  
                'created_day', 'created_dayofweek', 'created_dayofweekname', 'created_week', 'created_month', 'created_year', 
                'path_lvl_0', 'path_lvl_1', 'path_lvl_2']]
        return df


    @staticmethod
    def __get_dateslice_data(df: pd.DataFrame, date_column: str):
        date_dict = {
            'day': date_column + '_day',
            'dayofweek': date_column + '_dayofweek',
            'dayofweekname': date_column + '_dayofweekname',
            'week': date_column + '_week',
            'month': date_column + '_month',
            'year': date_column + '_year',
        }

        # Define time ranges
        today = datetime.today().date()
        yesterday = today - pd.DateOffset(days=1)
        current_week = today.isocalendar()[1]
        current_month = today.month
        current_year = today.year

        # Filter data by time ranges
        today_df = df[df[date_dict['day']] == today]
        yesterday_df = df[df[date_dict['day']] == yesterday]
        week_df = df[df[date_dict['week']] == current_week]
        month_df = df[df[date_dict['month']] == current_month]
        year_df = df[df[date_dict['year']] == current_year]

        return today_df, yesterday_df, week_df, month_df, year_df

    #Preprocees data that generate groupped table by orders (self.df dataframe contains 1 item for each row)
    @staticmethod
    def __get_convolutional_table(df):
        df = df.groupby('order_id')\
            .agg({
                'created': 'first', 
                'agent_name': 'first', 
                'companyType': 'first', 
                'assortment_name': lambda x: list(x),
                'state': 'first', 
                'quantity': 'sum', 
                'sum': 'first',
                'price': 'mean', 
                'city': 'first', 
                'volumes': lambda x: set(x), 
                'created_day': 'first',
                'created_dayofweek': 'first', 
                'created_dayofweekname': 'first', 
                'created_week': 'first',
                'created_month': 'first', 
                'created_year': 'first', 
                'path_lvl_0': lambda x: set(x), 
                'path_lvl_1': lambda x: set(x),
                'path_lvl_2': lambda x: set(x)
            })\
            .reset_index()
        return df
    
    #Group of methods that use in pd.DataFrame.apply() functions
    @staticmethod
    def _compare_city(row):
        if row['city'] == 'Город не указан':
            return row['found_city']
        else:
            return row['city']
        
    @staticmethod
    def _compare_path_depth(row):
        if pd.isna(row['path_lvl_2']):
            return row['path_lvl_1']
        else:
            return row['path_lvl_2']