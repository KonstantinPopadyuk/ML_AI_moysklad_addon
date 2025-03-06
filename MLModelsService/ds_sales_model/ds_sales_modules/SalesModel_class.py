import pandas as pd
import numpy as np
import time
import optuna
from scipy.stats import t as t_student
from decimal import Decimal

import sys
import os
path_str = os.sep.join(os.getcwd().split(os.sep)[:5])+'/'
sys.path.append(path_str)

from .loggermodels import LoggerModelsResults
from .sales_model_features_create import SalesDataFeatures
from .sales_strategies import ModelStrategy
from .traintestsplit_strategy_sales import TrainTestSplitStrategy


class TreeBoostedSalesModel():
    def __init__(self, 
                 df: pd.DataFrame, 
                 model_strategy: ModelStrategy, 
                 train_test_split_strategy: TrainTestSplitStrategy,
                 logs: LoggerModelsResults, 
                 num_features_blocks: int):
        
        self.df = df
        self.tree_algorithm = model_strategy.get_algorithm()
        self.model_name = model_strategy.get_name()
        self.train_test_split = train_test_split_strategy.get_algorithm()
        self.last_period_for_pred = train_test_split_strategy.get_last_period()
        self.split_name = train_test_split_strategy.get_name()
        
        self.optuna_objective = model_strategy.get_optuna_objective()
        self.result_logs=logs

        self.parametrs_list = []
        self.comb_len = num_features_blocks
        self.feature_test_size = 'min' if self.comb_len <= 4 else 'all'
        self.comb_count = 2**self.comb_len

        self.models_results = []
        self.selected_model_combination = None
        self.selected_model_features_dict_size = None 

        self.best_model_params = None
        self.best_cv_model = None
        self.selected_data_for_best_model = None

      
    def main_loop_with_cv(self, chunks: int, validation_size: int, cv_offset_list: list, verbose = True):
        self.parametrs_list = []
        for i, combination in enumerate(self.generate_binary_combinations(self.comb_len)):
            if verbose:
                print(f'Step {i+1}/{self.comb_count}', end="\r")
            data, params, model_params_number = SalesDataFeatures.create_example_data_with_features(self.df, combination, feature_test_size=self.feature_test_size)

            start_time = time.time()
            mse, _ = self._train_tree(data, cross_validation=True, chunks=chunks, validation_size=validation_size, cv_offset_list = cv_offset_list)
            end_time = time.time()
            execution_time = round((end_time - start_time), 3)
            
            params.extend([execution_time]) #index -3
            params.extend([model_params_number]) #index -2
            params.extend([mse]) #index -1
            self.parametrs_list.append(params)
    
    def _train_tree(self, data, cross_validation=False, chunks=5, validation_size=45, cv_offset_list = [30, 60, 90, 120], params=None, logs=False, cv_mar_er=False):
        mse_list = []
        margin_of_error_list = []

        if cross_validation:
            assert chunks <= len(cv_offset_list), f'Not enough periouds in offset list, chunks should be less or equal {len(cv_offset_list)=}'
            cv_offset_list = cv_offset_list[:chunks]
            self.chunks, self.validation_size, self.cv_offset_list = chunks, validation_size, cv_offset_list

            for cv_offset in cv_offset_list:
                train_data_day = data[:-cv_offset].copy()
                X_train, X_test, y_day_train, y_day_test = self.train_test_split(train_data=train_data_day, test_size=validation_size)
                mse, y_pred, model = self.tree_algorithm(X_train, X_test, y_day_train, y_day_test, params=params)
                lower_bound, upper_bound, margin_of_error = self.calculate_confidence_inteval(y_pred=y_pred, y_true=y_day_test)
                margin_of_error_list.append(margin_of_error)
                mse_list.append(mse)

            return np.mean(mse_list), pd.concat(margin_of_error_list, axis=1).mean(axis=1)
        else:
            train_data_day = data.copy()
            X_train, X_test, y_day_train, y_day_test = self.train_test_split(train_data=train_data_day, test_size=validation_size)
            mse, y_pred, model = self.tree_algorithm(X_train, X_test, y_day_train, y_day_test, params=params)
            mse_list.append(mse)
            if logs:
                self.result_logs.update(index=self.model_name, param='MSE_test', result='%.2E' % Decimal(np.mean(mse_list)))

            return np.mean(mse_list), y_pred, model
    

    def set_results_table(self):
        self.models_results = self.models_analysis_table(self.parametrs_list)
        self.models_results = self.models_results.sort_values(by='MSE', ascending=True)
        print(f'Worst MSE {self.models_results.MSE.max()}')
        print(f'Best  MSE {self.models_results.MSE.min()}')
        print(f'Worst time {self.models_results.fit_time.max()} seconds')
        print(f'Best  time {self.models_results.fit_time.min()} seconds')

    
    def select_top_model_vec(self, top_mse = 3, top_fit_time = 1):
        top_models = self.models_results.sort_values(by='MSE', ascending=True).head(top_mse).sort_values(by='fit_time', ascending=True).loc[:top_fit_time,:]
        selected_combinations = []
        for row in top_models.iloc[:,:-3].iterrows():
            selected_combinations.append(list(row[1]))
        #Take only 1 element. List and append for maybe more complex logic in model selection
        #------
        selected_combination = selected_combinations[0]
        #------
        selected_combination = [str(x) for x in selected_combination]
        comb_len = len(selected_combination)
        
        #hot fix (if - else) for goods model:
        if self.split_name == 'multi_goods_pred':
            features_dict_size = 'goods_model'
        else:
            features_dict_size = 'min' if comb_len <= 4 else 'all'

        self.result_logs.update(index=self.model_name, param='features_vec', result=str(selected_combination))

        self.selected_model_combination = selected_combination
        self.selected_model_features_dict_size = features_dict_size
        self.selected_data_for_best_model, _, _ = SalesDataFeatures.create_example_data_with_features(df=self.df, 
                                                                         selected_functions=self.selected_model_combination, 
                                                                         feature_test_size=self.selected_model_features_dict_size)
        
    def _manually_set_top_model_vec(self, vec: list[str]):
        if self.selected_model_combination is not None:
            self._backup_vec = self.selected_model_combination.copy()
        self.selected_model_combination = vec
        features_dict_size = 'min' if len(vec) <= 4 else 'all'
        self.selected_model_features_dict_size = features_dict_size
        self.selected_data_for_best_model, _, _ = SalesDataFeatures.create_example_data_with_features(df=self.df, 
                                                                         selected_functions=self.selected_model_combination, 
                                                                         feature_test_size=self.selected_model_features_dict_size)
    

    def start_optuna(self, data, n_trials=50):
        # Создаем исследование Optuna
        study = optuna.create_study(direction="maximize")
        objective = self.optuna_objective
        study.optimize(lambda trial: objective(trial, data, self._train_tree, self.chunks, self.validation_size, self.cv_offset_list), n_trials=n_trials)

        # Получаем наилучшие параметры и результат
        best_params = study.best_params
        self.best_model_params = best_params
        best_score = -study.best_value  # Переводим обратно в MSE

        self.result_logs.update(index=self.model_name, param='best_params', result=str(best_params))
        self.result_logs.update(index=self.model_name, param='MSE_crossval', result='%.2E' % Decimal(best_score))
        print("Лучшие параметры:", best_params)
        print("Лучший результат XGB VAL (MSE):", '%.2E' % Decimal(best_score))

        return best_params
    
    def get_best_model_pred_on_test(self, test_size):
        X_train, X_test, y_train, y_test = self.train_test_split(train_data=self.selected_data_for_best_model, test_size=test_size)

    
        mse, y_pred, self.best_cv_model = self._train_tree(data=self.selected_data_for_best_model, 
                                          cross_validation=False, 
                                          logs=False, 
                                          validation_size=test_size, 
                                          params=self.best_model_params)
        
        self.result_logs.update(index=self.model_name, param='MSE_test', result='%.2E' % Decimal(mse))
        print(f'MSE for day prediction with best XGB model: {mse}')

        return y_train, y_test, y_pred, mse
    
    def _predict_on_last_period(self):
        last_period = self.last_period_for_pred(self.selected_data_for_best_model)
        prediction = self.best_cv_model.predict(last_period)
        return prediction
    

    def calculate_confidence_inteval(self, y_pred, y_true):
        from scipy.stats import norm

        import scipy.stats as st
        # Остатки
        residuals = y_pred - y_true

        # Стандартное отклонение остатков
        std_residuals = np.std(residuals)

        # interval = st.t.interval(alpha=0.95, df=len(residuals)-1, loc=np.mean(residuals), scale=st.sem(residuals)) 

        # Доверительный интервал (95%)
        n = len(residuals)
        t_value = t_student.ppf(0.95, df=n-1)
        z_score = norm.ppf((1 + 0.95) / 2)
        z_score2 = norm.ppf(0.95)
        margin_of_error = t_value * std_residuals / np.sqrt(n)
        # print(f'{margin_of_error=}')
        # print(f'{(z_score * std_residuals).astype(float)=}')
        # print(f'{(z_score2 * std_residuals).astype(float)=}')

        margin_of_error = z_score * std_residuals
        # Доверительный интервал для прогнозов
        lower_bound, upper_bound = self.calculate_low_up_bounds(y_pred, margin_of_error, y_true.index)
        return lower_bound, upper_bound, margin_of_error
    
    def calculate_low_up_bounds(self, y_pred, margin_of_error, y_true_index):
        if self.split_name == 'multi_day_pred' or self.split_name =='multi_goods_pred':
            lower_bound = [np.round(np.array(item - margin_of_error),0) for item in y_pred]
            # lower_bound = pd.Series(lower_bound)
            # lower_bound.index = y_true_index
            lower_bound = pd.DataFrame(lower_bound, index=y_true_index)

            upper_bound = [np.round(np.array(item + margin_of_error),0) for item in y_pred]
            # upper_bound = pd.Series(upper_bound)
            # upper_bound.index = y_true_index
            upper_bound = pd.DataFrame(upper_bound, index=y_true_index)

        else:
            lower_bound = pd.Series(y_pred - margin_of_error)
            lower_bound.index = y_true_index
            upper_bound = pd.Series(y_pred + margin_of_error)
            upper_bound.index = y_true_index
        
        return lower_bound, upper_bound
    
    @staticmethod
    def generate_binary_combinations(num_digits):
        """
        Генерирует все возможные комбинации двоичных цифр заданной длины.
        """
        for i in range(2**num_digits):
            yield list(format(i, f"0{num_digits}b"))

    @staticmethod
    def models_analysis_table(parametrs):
        #найти самый длинный лист в табличке (должен быть последним)
        max = parametrs[-1]
        #взять от туда все строковые данные (все кроме последнего элемента)
        columns_names = max[:-3]
        #взять это значение как столбцы
        columns_names.extend(['MSE', 'params_num', 'fit_time'])
        models_dataframe = pd.DataFrame(columns=columns_names)

        #идти по элементам листа
        for item in parametrs:
            models_row = pd.DataFrame(data=[[0]*len(columns_names)], columns=columns_names)    
            #проверять есть ли каждая колонка в листе, если есть ставить 1
            for column in columns_names:
                if column in item:
                    models_row[column] = 1    
            #последнее значение массива записывать в колонку MSE
            models_row['MSE'] = item[-1]
            models_row['params_num'] = item[-2]
            models_row['fit_time'] = item[-3]
            models_dataframe = pd.concat([models_dataframe, models_row], ignore_index=True)
        
        models_dataframe = models_dataframe.sort_values(by='MSE', ascending=True).reset_index(drop=True)
        
        return models_dataframe