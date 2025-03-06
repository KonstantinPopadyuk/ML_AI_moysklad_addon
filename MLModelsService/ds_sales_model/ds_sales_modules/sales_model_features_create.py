import sys
import os

# Путь к корню проекта (на два уровня выше от текущего файла)
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_path)


import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from transformed_data import ProcessedData
from .sales_model_data import SalesModelData


class SalesDataFeatures():
    def __init__(self, df):
        self.raw_df = df.copy()

        self.daily_sales = self.create_daily_sales()
        self.daily_sales_dates = self.daily_sales.iloc[:,:1]

        self.df_with_features = self.daily_sales.copy()
        self.df_with_features.columns = [SalesModelData.translit_column_name(column) for column in self.df_with_features.columns]
        
        self.data_augmentation = None
        self.goods_features = None
        self.agents_features = None
        self.lag_features = None
        self.rolling_average_features = None
        self.means_features = None
        self._multi_dummies_features = None
        self._onehot_dummies_features = None

        self.features_list = []
        self.params_count = len(self.df_with_features.columns)

        self.multi_label_dummies = ['agent_name']
        self.onehot_dummies_list = ['created_dayofweekname']

        self.smth_merge = False

    def set_data_augmentation(self):
        """
        NEED TO DESCRIBE FUNC
        """
        if self.data_augmentation is None: 
            self.data_augmentation = self._create_data_augmentation()
            if self.raw_df['created_year'].min() > 2022:
                self.raw_df = pd.concat([self.raw_df, self.data_augmentation], ignore_index=True).sort_values('created', ascending=True).reset_index(drop=True)
                self.daily_sales = self.create_daily_sales()
                self.daily_sales_dates = self.daily_sales.iloc[:,:1]
                self.df_with_features = self.daily_sales.copy()
            else:
                print('For augmentation actual df should start at 2023, previously data do not accepted')



    def set_goods_features(self):
        """
        NEED TO DESCRIBE FUNC
        """
        if self.goods_features is None: 
            self.goods_features = self._create_goods_features()
            self.features_list.append(self.goods_features)
            self.smth_merge = True

    def set_agents_features(self):
        """
        NEED TO DESCRIBE FUNC
        """
        if self.agents_features is None:
            self.agents_features = self._create_agents_features()
            self.features_list.append(self.agents_features)
            self.smth_merge = True
    

    def set_lag_features(self, lag_sizes=[7, 14, 30, 60]):
        """
        NEED TO DESCRIBE FUNC
        """
        if self.lag_features is None:
            self.lag_features = self._create_lag_features(lag_sizes=lag_sizes)
            self.features_list.append(self.lag_features)
            self.smth_merge = True

    def set_rolling_average_features(self, window_sizes=[2, 3, 4, 5, 7, 14, 30, 60, 90, 120, 180]):
        """
        NEED TO DESCRIBE FUNC
        """
        if self.rolling_average_features is None: 
            self.rolling_average_features = self._create_rolling_average_features(window_sizes=window_sizes)
            self.features_list.append(self.rolling_average_features)
            self.smth_merge = True

    def set_means_features(self):
        """
        NEED TO DESCRIBE FUNC
        """
        if self.means_features is None:
            self.means_features = self._create_means_features()
            self.features_list.append(self.means_features)
            self.smth_merge = True

    def set_multi_dummy_features(self):
        """
        NEED TO DESCRIBE FUNC
        """
        if self._multi_dummies_features is None:
            #Create mulilabel first            
            for col in self.multi_label_dummies:
                mlb = MultiLabelBinarizer()
                dummies = pd.DataFrame(
                    data=mlb.fit_transform(self.df_with_features[col]), 
                    columns=mlb.classes_, 
                    index=self.df_with_features.index
                    )
                self.df_with_features = self.df_with_features.join(dummies)

            self.df_with_features = self.df_with_features.drop(self.multi_label_dummies, axis=1)

            self._multi_dummies_features = True
            self.params_count = len(self.df_with_features.columns)
            #hot fix, need to set some flag
            #----------------
            self.df_with_features.columns = [SalesModelData.translit_column_name(column) for column in self.df_with_features.columns]
            #----------------
            #Next row is a hot fix for not correct storage of 'agent_names', need to rewrite this logic (only unique names or use agent_id instead)
            #----------------
            self.df_with_features.columns = [f'{column}_{i}' if column not in ['sum', 'created_day', 'agent_name', 'created_dayofweekname'] else column for i, column in enumerate(self.df_with_features.columns)]
            #----------------

    def set_onehot_dummy_features(self):
        """
        NEED TO DESCRIBE FUNC
        """
        if self._onehot_dummies_features is None:
            #Create one-hot label
            self.df_with_features = pd.get_dummies(self.df_with_features, columns=self.onehot_dummies_list)
            
            self._onehot_dummies_features = True
            self.params_count = len(self.df_with_features.columns)
            #hot fix, need to set some flag
            #----------------
            self.df_with_features.columns = [SalesModelData.translit_column_name(column) for column in self.df_with_features.columns]
            #----------------
            #Next row is a hot fix for not correct storage of 'agent_names', need to rewrite this logic (only unique names or use agent_id instead)
            #----------------
            self.df_with_features.columns = [f'{column}_{i}' if column not in ['sum', 'created_day', 'agent_name', 'created_dayofweekname'] else column for i, column in enumerate(self.df_with_features.columns)]
            #----------------
    
    def merge_features(self):
        """
        Merging all previously created features
        Working data will be availible in self.df_with_features

        """
        if self._multi_dummies_features is None:
            self.df_with_features = self.df_with_features.drop(self.multi_label_dummies, axis=1)
            self.params_count = len(self.df_with_features.columns)

        if self._onehot_dummies_features is None:
            self.df_with_features = self.df_with_features.drop(self.onehot_dummies_list, axis=1)
            self.params_count = len(self.df_with_features.columns)            

        if self.smth_merge:
            for table in self.features_list:
                self.df_with_features = pd.merge(left=self.df_with_features, right=table, on='created_day')
            self.smth_merge = False
            self.params_count = len(self.df_with_features.columns)
            #hot fix, need to set some flag
            #----------------
            self.df_with_features.columns = [SalesModelData.translit_column_name(column) for column in self.df_with_features.columns]
            #----------------

            #Next row is a hot fix for not correct storage of 'agent_names', need to rewrite this logic (only unique names or use agent_id instead)
            #----------------
            self.df_with_features.columns = [f'{column}_{i}' if column not in ['sum', 'created_day', 'agent_name', 'created_dayofweekname'] else column for i, column in enumerate(self.df_with_features.columns)]
            #----------------
        elif (self._onehot_dummies_features is None) \
            & (self._multi_dummies_features is None) \
            & (self.data_augmentation is None):
            print('Nothing new to merge')

    def get_data_with_all_features(self):
        """
        NEED TO DESCRIBE FUNC
        """
        #need to add all setters
        self.set_goods_features()
        self.set_agents_features()
        self.set_lag_features()
        self.set_rolling_average_features()
        self.set_means_features()
        self.merge_features()
        return self.df_with_features
    
    def create_daily_sales(self):
        """
        NEED TO DESCRIBE FUNC
        """
        columns_list = [
            'order_id',
            'agent_name', 
            'created_day', 
            'created_week', 
            'created_month', 
            'created_year',
            'day', 
            'companyType', 
            'created_dayofweekname']

        tr = self.raw_df.groupby(columns_list).agg({'sum': 'first'}).reset_index().copy()
        tr['created_day'] = pd.to_datetime(tr['created_day'])

        aggregation = {
            'agent_name': lambda x: list(x), 
            'created_week':'first', 
            'created_month':'first', 
            'created_year':'first',
            'day':'first', 
            'created_dayofweekname':'first',
            'sum': 'sum'
        }

        daily_sales = tr.groupby('created_day').agg(aggregation).reset_index()
        daily_sales = daily_sales.sort_values(by='created_day').reset_index(drop=True)
        return daily_sales
    
    def _create_data_augmentation(self, noise_distr='normal'):
        #Data augmentation
        num_augm_months = 1
        augm_month = 12 - (num_augm_months - 1)
        data_aug = self.raw_df.query(f'created_year == 2023 and created_month >= {augm_month} and created_month <= 12').copy()

        #dates engineering
        data_aug.loc[:, 'created'] = data_aug['created'].apply(lambda x: x - pd.Timedelta(days=365))
        data_aug = ProcessedData._ProcessedData__add_dates_columns(df=data_aug, date_column='created')
        data_aug.loc[:, 'day'] = data_aug['created_day'].dt.day

        #names engineering
        data_aug.loc[: ,'order_id'] = data_aug['order_id'].apply(lambda x: f'(augm){x}')
        data_aug.loc[: ,'agent_name'] = data_aug['agent_name'].apply(lambda x: f'(augm){x}')

        #sum and quantity changes
        np.random.seed(42)
        decrise_percent = 0.4
        multiplicator = 1 - decrise_percent
        random_noise_uniform = 0.15
        random_noise_normal_std = 0.05
        random_noise_normal_mean = 0
    
        if noise_distr == 'normal':
            data_aug.loc[: ,'quantity'] = data_aug['quantity'].apply(
                lambda x: int(x*multiplicator + x*multiplicator*np.random.normal(random_noise_normal_mean, random_noise_normal_std))
                    )
            data_aug.loc[: ,'quantity'] = data_aug['quantity'].apply(lambda x: 1 if x<=0 else x)

            data_aug.loc[: ,'sum'] = data_aug['sum'].apply(
                lambda x: round(x*multiplicator + x*multiplicator*np.random.normal(random_noise_normal_mean, random_noise_normal_std), 0)
                )
            mean_sum = data_aug['sum'].mean()
            data_aug.loc[data_aug['sum'] <= 0, 'sum'] = mean_sum

        else:
            data_aug.loc[: ,'quantity'] = data_aug['quantity'].apply(
                lambda x: int(x*multiplicator + x*multiplicator*np.random.uniform(-random_noise_uniform, random_noise_uniform))
                    )
            data_aug.loc[: ,'quantity'] = data_aug['quantity'].apply(lambda x: 1 if x<=0 else x)
            
            data_aug.loc[: ,'sum'] = data_aug['sum'].apply(
                lambda x: round(x*multiplicator + x*multiplicator*np.random.uniform(-random_noise_uniform, random_noise_uniform), 0)
                )
            mean_sum = data_aug['sum'].mean()
            data_aug[data_aug['sum'] <= 0]['sum'] = mean_sum

        data_aug = data_aug.sort_values(by='created', ascending=False)

        return data_aug

    def __create_agents_table(self, df):
        '''
        Create agents transpose table (created_day, all_agents*3)
        Data - sales quantity, day_between_purshases, total sum

        In fact part with only_one_order was depricated, because we drop all columns with zeros
        In this version this code not deleted because it can be use if dont drop this columns
        '''
        #create table
        agents_table = df[['order_id', 'created_day', 'agent_name', 'quantity', 'sum']].copy()
        agents_table = agents_table.sort_values(by='created_day').reset_index(drop=True)

        #agg data (sum quantity and orders total amount)
        agents_table = agents_table.groupby(['order_id', 'created_day', 'agent_name']).agg({'sum':'first', 'quantity':'sum'}).reset_index()
        agents_table = agents_table.groupby(['created_day', 'agent_name']).agg({'sum':'sum', 'quantity':'sum'}).reset_index()
        agents_table = agents_table.drop(agents_table[agents_table['sum'] == 0].index)
        agents_table = agents_table.reset_index(drop=True)

        #create each client order frequancy
        agents_table['days_between_purchases'] = agents_table.groupby('agent_name')['created_day'].diff().dt.days
        agents_table.fillna(0, inplace=True)
        #find clients with only one order. later manually count days between orders
        only_one_order = agents_table.groupby('agent_name').agg({'created_day':['count', 'first']}).reset_index().copy()
        only_one_order.columns = [f'{col[0]}_{col[1]}' for col in only_one_order.columns]
        only_one_order = only_one_order[only_one_order['created_day_count'] == 1]
        only_one_order = only_one_order.drop('created_day_count', axis=1)
        only_one_order['agent_name_'] = only_one_order['agent_name_'].apply(lambda x: f'days_between_purchases_{x}')

        #make finaly pivot table
        agents_table_transposed = agents_table.pivot_table(index='created_day', columns='agent_name', values=['quantity', 'days_between_purchases', 'sum'], aggfunc='sum', fill_value=0)
        agents_table_transposed.columns = [f'{col[0]}_{col[1]}' for col in agents_table_transposed.columns]
        agents_table_transposed = agents_table_transposed.sort_values(by='created_day')
        agents_table_transposed.reset_index(inplace=True)

        return agents_table_transposed, only_one_order
    
    def _create_agents_features(self, verbose=False):
        """
        NEED TO DESCRIBE FUNC
        """
        agents_table_transposed, only_one_order = self.__create_agents_table(self.raw_df)
        agents_table_transposed, to_drop = self.drop_null_columns(agents_table_transposed)

        # fill_orderdays_onetime_client(only_one_order)
        columns_days_between = [x for x in agents_table_transposed.columns if 'days_between_purchases_' in x]
        for i, column in enumerate(columns_days_between):
            if verbose:
                print(f'Currently we are at {i+1}/{len(columns_days_between)}', end="\r")
            agents_table_transposed[column] = self.__transform_all_days_between(agents_table_transposed[column].copy())


        agents_table_transposed, to_drop = self.drop_null_columns(agents_table_transposed)

        return agents_table_transposed

    def _create_goods_features(self):
        '''
        Create transpose table (created_day, all_items)
        Data - sales quantity
        '''
        goods_table = self.raw_df[['created_day', 'assortment_name', 'quantity']].copy()
        goods_table = goods_table.sort_values(by='created_day')
        goods_table = goods_table.pivot_table(index='created_day', columns='assortment_name', values='quantity', aggfunc='sum', fill_value=0).reset_index()
        goods_table.columns.name = None
        return goods_table

    def _create_means_features(self):
        """
        NEED TO DESCRIBE FUNC
        """
        if self.agents_features is None:
            df = self._create_agents_features()
        else:
            df = self.agents_features
        means = pd.DataFrame(df.replace(0,np.NaN).mean()).T
        means = means.drop('created_day', axis=1)
        means.columns = [f'mean_{col}' for col in means.columns]
        means_repeated = pd.concat([means] * len(df), ignore_index=True)
        means_repeated = means_repeated.apply(pd.to_numeric)
        means_repeated.insert(0, 'created_day', self.daily_sales_dates)
        return means_repeated
    
    def _create_rolling_average_features(self, window_sizes=[2, 3, 4, 5, 7, 14, 30, 60, 90, 120, 180]):
        """
        NEED TO DESCRIBE FUNC
        neew to disxribe what columns it returning and expecting
        """
        daily_sales = self.daily_sales

        rolling = pd.DataFrame()
        for window_size in window_sizes:
            rolling_avg_col = f'avg_sum_last_{window_size}_days'
            rolling[rolling_avg_col] = daily_sales['sum'].rolling(window=window_size).mean()
        
        rolling.insert(0, 'created_day', self.daily_sales_dates)
        rolling = rolling.fillna(0.0)
        return rolling
    
    def _create_lag_features(self, lag_sizes = [7, 14, 30, 60]):
        """
        NEED TO DESCRIBE FUNC
        """
        daily_sales = self.daily_sales
        
        target_map = daily_sales['sum'].to_dict()
        lags_table = pd.DataFrame()
        
        for lag in lag_sizes:
            lag_name = f'lag_{lag}'
            lags_table[lag_name]=(daily_sales.index - lag).map(target_map)
        
        lags_table.insert(0, 'created_day', self.daily_sales_dates)
        lags_table = lags_table.fillna(0.0)
        
        return lags_table
    

    def fill_orderdays_onetime_client(self, only_one_order):
        '''
        For client with only 1 order for all time
        this function make some mark (set value == 1)
        This is nessesary to avoid null columns and for correct work
        of 'def transform_all_days_between(lst):
        '''
        def update_value(df, agent_name, date):
            if agent_name in df.columns:
                df.loc[df['created_day'] == date, agent_name] = 1

        for row in only_one_order.iterrows():
            agent_name = row[1]['agent_name_']
            date = row[1]['created_day_first'] 
            update_value(self.agents_features, agent_name, date)

    @staticmethod
    def _transform_first_days_between(lst):
        '''
        Part of main function 'def transform_all_days_between(lst):'
        Fill first days till the first purchase day

        Test example:
        test = [0, 0, 0, 0, 0, 5, 0, 0, 0, 4, 0, 2, 0, 0, 3]
        transform_all_days_between(test)

        [0, 0, 0, 0, 0, 5, 0, 0, 0, 4, 0, 2, 0, 0, 3] -> [0, 1, 2, 3, 4, 5, 0, 0, 0, 4, 0, 2, 0, 0, 3]
        '''
        import copy

        index = None
        value = None
        #Try to find the day with the first sale day
        for i, item in enumerate(lst):
            if item != 0:
                index, value = i, item
                break
        if value == None:
            # print('Something defenetly goes wrong, all rows == 0')
            return lst
        value_range = int(copy.deepcopy(value))
        #Go backward and fill the values with days
        for i in range(value_range):
            value-=1
            index-=1
            if index < 0:
                # print('Index out of bounce, something wrong with days')
                break        
            lst[index] = value

        return lst

    @staticmethod
    def __transform_all_days_between(lst):
        '''
        Fill all days after first purchase

        Test example:
        data = {
        'Values_1': [0, 0, 55, 0, 0, 5, 0, 3, 0, 4, 0, 2, 0, 0, 3, 0, 0],
        'Values_2': [0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 4, 0, 2, 0, 0, 3],
        'Values_3': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'Values_4': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        }

        df = pd.DataFrame(data)

        df = pd.DataFrame(data)
        df_new = pd.DataFrame()
        for column in df.columns:
            df_new[column] = transform_allother_days_between(df[column])

        df_new

        [0, 0, 0, 0, 3, 0, 0, 0, 4, 0, 2, 0, 0, 3]
                            ||
                            \/ 
        [0, 0, 1, 2, 3, 1, 2, 3, 4, 1, 2, 1, 2, 3]

        Note: This function dont use 'created_date' so in fact 
        it will be difference in rows, not in dates.
        so it may cause come wrong data if there was periods with no sales
        and rows with this dates just don't exist in table
        '''
        lst = SalesDataFeatures._transform_first_days_between(lst)
        count = 0
        new_lst = []
        first_order = True
        for val in lst:
            if val == 0 and not first_order:
                count += 1
                new_lst.append(count)
            else:
                if val != 0:
                    first_order = False
                count = 0
                new_lst.append(val)

        return new_lst
    
    @staticmethod
    def drop_null_columns(df, verbose=False):
        '''
        Drop all columns where all rows == 0 

        Note: if this function will make any changes 
        something maybe wrong in data preparing process. 
        And mb it's need some more cautious review in 'to_drop' element

        In case where days_between drops - everything is ok
        '''
        to_drop = df.columns[(df == 0).all()]
        result = df.drop(to_drop, axis=1)
        if verbose:
            if to_drop.empty:
                print('Zero columns have been dropped')
            else:
                print('There was smth to drop, need to research')
        return result, to_drop
    
    @staticmethod
    def create_example_data_with_features(df, selected_functions: list, feature_test_size):
        """
        Генерирует данные с определенным набором фичей
        """

        use_features = []
        features_class = SalesDataFeatures(df)

        all_features_dict = {
            0: features_class.set_data_augmentation,
            1: features_class.set_goods_features, #probably can cause data leak because of data augmentation
            2: features_class.set_agents_features,
            3: features_class.set_lag_features,
            4: features_class.set_rolling_average_features,
            # 5: features_class.set_means_features, #need to delete it, dont have any affect 
            5: features_class.set_onehot_dummy_features,
            6: features_class.set_multi_dummy_features
        }

        min_features_dict = {
            0: features_class.set_data_augmentation,
            1: features_class.set_lag_features,
            2: features_class.set_rolling_average_features,
            3: features_class.set_onehot_dummy_features,
        }

        #need to find a more elegant way to choose the creation mechanism; currently implementation is a kind of 'hot fix'
        #also need to add rolling aver and lag features to goods, but with dropping. dont sure that in existing code it will work without bugs
        min_multygoods_strategy_dict = {
            0: features_class.set_onehot_dummy_features,
            #2: features_class.set_agents_features, #to much time consuming, maby will work with LightGMB
            1: features_class.set_rolling_average_features,
        }
        
        #this if-else is 'hot fix' to implement mulit_goods_7_30_60 model
        if feature_test_size != 'goods_model':
            features_dict = min_features_dict if feature_test_size == 'min' else all_features_dict
        else:
            features_dict = min_multygoods_strategy_dict

        for i, key in enumerate(selected_functions):
            if key == '1':
                use_features.append(features_dict[i].__name__)
                features_dict[i]()
            
        features_class.merge_features()
        
        return features_class.df_with_features, use_features, features_class.params_count