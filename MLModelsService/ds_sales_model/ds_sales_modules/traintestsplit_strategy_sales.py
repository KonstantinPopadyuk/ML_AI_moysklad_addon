from abc import ABC, abstractmethod
import pandas as pd

from .sales_model_features_create import SalesDataFeatures

class TrainTestSplitStrategy(ABC):
    @abstractmethod
    def get_algorithm(self):
        pass  

    @abstractmethod
    def get_name(self):
        pass    
    
    @abstractmethod
    def get_last_period(self):
        pass

class OneDayPredictStrategy(TrainTestSplitStrategy):
    def get_algorithm(self):
        return self.get_train_test_data
    
    def get_name(self):
        return 'one_day_pred'
    
    def get_last_period(self):
        return None
    
    @staticmethod
    def get_train_test_data(train_data, test_size):
    
        train_size = len(train_data) - test_size
        X_train = train_data.iloc[:train_size].drop(['sum', 'created_day'], axis=1).copy()
        X_test = train_data.iloc[train_size:-1].drop(['sum', 'created_day'], axis=1).copy()
        y_day_train = train_data.iloc[1:train_size+1]['sum'].copy()
        y_day_test = train_data.iloc[train_size+1:]['sum'].copy()

        return X_train, X_test, y_day_train, y_day_test
    

class MultiPeriodPredictStrategy(TrainTestSplitStrategy):
    def __init__(self, rolling_windows) -> None:
        super().__init__()
        self.rolling_windows = rolling_windows
        self.last_period = None
    
    def get_algorithm(self):
        return self.get_train_test_data
    
    def get_name(self):
        return 'multi_day_pred'
    
    def get_last_period(self, train_data):
        for window in self.rolling_windows:
            train_data[f'sum_{window}_days'] = train_data['sum'].sort_index(ascending=False).rolling(window=window).sum().sort_index(ascending=True)

        drop_X = [f'sum_{window}_days' for window in self.rolling_windows]
        drop_X.extend(['created_day'])

        self.last_period = train_data.tail(1).drop(drop_X, axis=1).copy()
        return self.last_period
    
    def get_train_test_data(self, train_data, test_size):
        train_size = len(train_data) - test_size - self.rolling_windows[-1]
        for window in self.rolling_windows:
            train_data[f'sum_{window}_days'] = train_data['sum'].sort_index(ascending=False).rolling(window=window).sum().sort_index(ascending=True)

        drop_X = [f'sum_{window}_days' for window in self.rolling_windows]
        drop_X.extend(['created_day'])
        take_y = [f'sum_{window}_days' for window in self.rolling_windows]
        
        X_train = train_data.iloc[:train_size].drop(drop_X, axis=1).copy()
        X_test = train_data.iloc[train_size:-(self.rolling_windows[-1]+1)].drop(drop_X, axis=1).copy()
        y_day_train = train_data.iloc[1:train_size+1].loc[:,take_y].copy()
        y_day_test = train_data.iloc[train_size+1:-self.rolling_windows[-1]].loc[:,take_y].copy()

        return X_train, X_test, y_day_train, y_day_test
    
class GoodsPredictStrategy(TrainTestSplitStrategy):
    def __init__(self, df, rolling_windows) -> None:
        super().__init__()
        self.raw_df = df
        self.rolling_windows = rolling_windows
        self.last_period = None
    
    def get_algorithm(self):
        return self.get_train_test_data  

    def get_name(self):
        return 'multi_goods_pred'
    
    def get_last_period(self):
        return self.__get_last_period
    
    def __get_last_period(self, train_data):
        train_index = train_data.index
        train_data, adding_goods_table, columns_to_drop = self.preprocess_train_data(train_data, train_index)

        for window in self.rolling_windows:
            for column in columns_to_drop:
                train_data[f'{column}_sum_{window}_days'] = train_data[column].sort_index(ascending=False).rolling(window=window).sum().sort_index(ascending=True)

        drop_X = [f'{column}_sum_{window}_days' for window in self.rolling_windows for column in columns_to_drop]
        drop_X.extend(['created_day'])

        self.last_period = train_data.tail(1).drop(drop_X, axis=1).copy()

        return self.last_period
    
    def get_train_test_data(self, train_data, test_size):
        train_index = train_data.index
        train_data, adding_goods_table, columns_to_drop = self.preprocess_train_data(train_data, train_index)

        train_size = len(train_data) - test_size - self.rolling_windows[-1]
        for window in self.rolling_windows:
            for column in columns_to_drop:
                train_data[f'{column}_sum_{window}_days'] = train_data[column].sort_index(ascending=False).rolling(window=window).sum().sort_index(ascending=True)

        drop_X = [f'{column}_sum_{window}_days' for window in self.rolling_windows for column in columns_to_drop]
        drop_X.extend(['created_day'])
        take_y = [f'{column}_sum_{window}_days' for window in self.rolling_windows for column in columns_to_drop]
        
        X_train = train_data.iloc[:train_size].drop(drop_X, axis=1).copy()
        X_test = train_data.iloc[train_size:-(self.rolling_windows[-1]+1)].drop(drop_X, axis=1).copy()
        y_day_train = train_data.iloc[1:train_size+1].loc[:,take_y].copy()
        y_day_test = train_data.iloc[train_size+1:-self.rolling_windows[-1]].loc[:,take_y].copy()

        return X_train, X_test, y_day_train, y_day_test
    
    def preprocess_train_data(self, df, train_index):
        preprocess_df = df.loc[train_index, :]

        df_for_features = self.raw_df.copy()
        features_class = SalesDataFeatures(df_for_features)
        #need to fix, after refactor SalesDataFeatures
        #use instead _create_goods_features directly
        #now its impossible because of columns translit
        #------------
        features_class.set_goods_features()
        features_class.merge_features()
        adding_goods_table = features_class.df_with_features.drop(columns=['created_day', 'created_week_1', 'created_month_2', 'created_year_3', 'day_4',
       'sum'])
        #------------
        adding_goods_table = adding_goods_table.loc[train_index, :]
        columns_to_drop = adding_goods_table.columns
        

        preprocess_df = pd.concat([preprocess_df, adding_goods_table], axis=1)

        return preprocess_df, adding_goods_table, columns_to_drop

    