import pickle
from .database import read_data_sync
from ds_sales_model.ds_sales_modules import SalesModelData
import pandas as pd
import os
from pathlib import Path

class SalesPredsData:
    base_dir = Path(__file__).resolve().parent.parent  # Переходим на два уровня выше
    multi_goods_preds_file = base_dir / 'ds_sales_model' / 'sales_multi_goods_7_30-60_predictions.pkl'
    stock_query = 'SELECT * FROM stock;'
    
    def __init__(self) -> None:
        """Initialization of the SalesPredsData class.
        
        Loads sales prediction data from a file and initializes
        variables for storing actual stock data and merged data.
        """
        self.sales_multi_goods_predictions = self.load_df_pkl(self.multi_goods_preds_file)
        self.actual_stock_data = None
        self.merged_goods_and_preds = None

    def get_merged_goods_and_preds(self, update=False):
        """Retrieves merged data of goods and predictions.

        If the update parameter is set to True, it updates all data.
        If the actual stock data has not been loaded yet, it calls the
        _update_data method to load it.

        Returns:
            pd.DataFrame: Merged data of goods and predictions.
        """
        if update:
            self.update_all_data()

        if self.actual_stock_data is None:
            self._update_data()

        preds = self.sales_multi_goods_predictions.reset_index(names='name')

        assert preds is not None, f'Predictions cannot be empty {__class__}{__name__}'
        assert self.actual_stock_data is not None, f'Stock table in db cannot be empty {__class__}{__name__}'

        self.merged_goods_and_preds = pd.merge(preds, self.actual_stock_data, 'left', on='name')
        self.merged_goods_and_preds = self._preprocess_goods_preds_data(self.merged_goods_and_preds)
        self.merged_goods_and_preds = self.merged_goods_and_preds.fillna('')
        return self.merged_goods_and_preds

    def update_all_data(self) -> None:
        """Updates all data, including actual stock data and predictions.

        Calls methods to update stock data and predictions.
        """
        self._update_data()
        self._update_predictions()

    def _update_predictions(self):
        """Updates sales prediction data from the file.

        Loads new prediction data from the specified file.
        """
        self.sales_multi_goods_predictions = self.load_df_pkl(self.multi_goods_preds_file)

    def _update_data(self):
        """Updates actual stock data.

        Calls the method to load stock data from the database.
        """
        self._update_stock_data()

    def _update_stock_data(self):
        """Loads actual stock data from the database.

        Executes an SQL query to retrieve stock data and
        preprocesses it.
        """
        self.actual_stock_data = read_data_sync(query=self.stock_query)
        self.actual_stock_data = self._preprocess_stock_data(self.actual_stock_data)

    @staticmethod
    def _preprocess_stock_data(df):
        """Preprocesses stock data.

        Retains only necessary columns and removes duplicates.
        Applies transliteration to product names.

        Args:
            df (pd.DataFrame): Stock data.

        Returns:
            pd.DataFrame: Preprocessed stock data.
        """
        df = df[['name', 'stock']]
        df.loc[:, 'name'] = df['name'].apply(lambda x: SalesModelData.translit_column_name(x))
        df = df[~df.name.duplicated()]
        return df
    
    @staticmethod
    def _preprocess_goods_preds_data(df):
        """Preprocesses goods and predictions data.

        Calculates the difference between actual stock and predictions
        for 7, 30, and 60 days.

        Args:
            df (pd.DataFrame): Goods and predictions data.

        Returns:
            pd.DataFrame: Preprocessed goods and predictions data.
        """
        try:
            df['after_7_days_pred'] = df['stock'] - df['7_preds']
            df['after_30_days_pred'] = df['stock'] - df['30_preds']
            df['after_60_days_pred'] = df['stock'] - df['60_preds']
        except Exception as e:
            print(f'Something went wrong with column names in the prediction table, {e}')
        finally:
            return df
    
    @staticmethod
    def load_df_pkl(file_link: str) -> pd.DataFrame:
        """Loads a DataFrame from a pickle file.

        Args:
            file_link (str): Path to the file.

        Returns:
            pd.DataFrame: Loaded data.
        """
        with open(file_link, 'rb') as file:
            df = pickle.load(file)
        return df
    
class SalesStockReports:
    def __init__(self, df: SalesPredsData, update: bool = False) -> None:
        """Initialization of the SalesStockReports class.

        Args:
            df (SalesPredsData): Object containing sales and predictions data.
            update (bool): Flag for updating data (default is False).
        """
        self.merged_goods_and_preds = None
        self.df = df
        self.update = update

    def get_full_table(self) -> pd.DataFrame:
        """Retrieves the full table with goods and predictions data.

        If the data has already been loaded, it returns it. Otherwise,
        it loads data using the get_merged_goods_and_preds method.

        Returns:
            pd.DataFrame: Full table with data.
            Wich contains this columns:
             - "name": position name
             - "7_preds": sales amount predictions in items for nearest 7 days
             - "30_preds": sales amount predictions in items for nearest 30 days
             - "60_preds": sales amount predictions in items for nearest 60 days
             - "stock": stock amount for current date
             - "after_7_days_pred": available amount after 7 days minus predictions
             - "after_30_days_pred": available amount after 7 days minus predictions
             - "after_60_days_pred": available amount after 7 days minus predictions
        """
        if self.merged_goods_and_preds is not None:
            df = self.merged_goods_and_preds
        else:
            df = self.df.get_merged_goods_and_preds(self.update)

        # I don't know why, but simple df.round(2) - works unpredictably
        df = df.applymap(lambda x: round(x, 2) if isinstance(x, (int, float)) else x)

        return df
    
    def get_N_days_need_to_buy_report(self, n: int) -> pd.DataFrame:
        """Retrieves a report on goods that need to be purchased in N days.

        Filters the data to keep only those goods for which
        the prediction for N days is less than zero.

        Args:
            n (int): Number of days for the prediction.

        Returns:
            pd.DataFrame: Report on goods that need to be purchased.
        """
        if self.merged_goods_and_preds is not None:
            df = self.merged_goods_and_preds
        else:
            df = self.df.get_merged_goods_and_preds(self.update)

        df[f'after_{n}_days_pred'] = pd.to_numeric(df[f'after_{n}_days_pred'])

        df = df[df[f'after_{n}_days_pred'] < 0][['name', 'stock', f'{n}_preds', f'after_{n}_days_pred']]

        # I don't know why, but simple df.round(2) - works unpredictably
        df = df.applymap(lambda x: round(x, 2) if isinstance(x, (int, float)) else x)

        return df