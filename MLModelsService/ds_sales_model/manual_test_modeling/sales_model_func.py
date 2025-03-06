import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import xgboost as xgb
from xgboost import XGBRegressor
import lightgbm as ltb
from catboost import Pool, CatBoostRegressor
from sklearn.metrics import mean_squared_error

from sales_model_features_create import SalesDataFeatures

from scipy.stats import t



def get_train_test_data(train_data, test_size=45):
    
    train_size = len(train_data) - test_size
    X_train = train_data.iloc[:train_size].drop(['sum', 'created_day'], axis=1).copy()
    X_test = train_data.iloc[train_size:-1].drop(['sum', 'created_day'], axis=1).copy()
    y_day_train = train_data.iloc[1:train_size+1]['sum'].copy()
    y_day_test = train_data.iloc[train_size+1:]['sum'].copy()

    return X_train, X_test, y_day_train, y_day_test

def train_default_XGBRegressor(X_train, X_test, y_train, y_test, params=None):
    if params is None:
        model = xgb.XGBRegressor(early_stopping_rounds=50)
    else:
        model = xgb.XGBRegressor(**params, early_stopping_rounds=50)

    model.fit(X_train, y_train, eval_set=[(X_train, y_train),(X_test, y_test)], verbose=False)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    return mse, y_pred, model

def train_default_LGBMRegressor(X_train, X_test, y_train, y_test, params=None):
    if params is None:
        model = ltb.LGBMRegressor(verbosity=-1)
    else:
        model = ltb.LGBMRegressor(**params, verbosity=-1)

    callbacks = [ltb.early_stopping(stopping_rounds=50, verbose=False)]
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], callbacks=callbacks)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    return mse, y_pred, model

def train_default_CatBoost(X_train, X_test, y_train, y_test, params=None):
    if params is None:
        model = CatBoostRegressor(verbose=False, cat_features=[], early_stopping_rounds = 20)
    else:
        model = CatBoostRegressor(**params, verbose=False, cat_features=[], early_stopping_rounds = 20)
    
    train_pool = Pool(X_train, y_train)
    test_pool = Pool(X_test) 
    eval_pool = Pool(X_test, y_test)
    
    model.fit(train_pool, eval_set=eval_pool)
    y_pred = model.predict(test_pool)
    mse = mean_squared_error(y_test, y_pred)

    return mse, y_pred, model

def train_xgboost(data, cross_validation=False, chunks=5, validation_size=45, cv_offset_list = [30, 60, 90, 120], params=None):
    train_data_day = data.copy()
    mse_list = []
    margin_of_error_list = []
    
    assert chunks <= len(cv_offset_list), f'Not enough periouds in offset list, chunks should be less or equal {len(cv_offset_list)=}'
    cv_offset_list = cv_offset_list[:chunks]

    if cross_validation:
        for cv_offset in cv_offset_list:
            train_data_day = data[:-cv_offset].copy()
            X_train, X_test, y_day_train, y_day_test = get_train_test_data(train_data=train_data_day, test_size=validation_size)
            mse, y_pred, model = train_default_XGBRegressor(X_train, X_test, y_day_train, y_day_test, params=params)
            lower_bound, upper_bound, margin_of_error = calculate_confidence_inteval(y_pred=y_pred, y_true=y_day_test)
            margin_of_error_list.append(margin_of_error)
            mse_list.append(mse)
    else:
        X_train, X_test, y_day_train, y_day_test = get_train_test_data(train_data=train_data_day, test_size=validation_size)
        mse, y_pred, model = train_default_XGBRegressor(X_train, X_test, y_day_train, y_day_test, params=params)
        lower_bound, upper_bound, margin_of_error = calculate_confidence_inteval(y_pred=y_pred, y_true=y_day_test)
        margin_of_error_list.append(margin_of_error)
        mse_list.append(mse)

    return np.mean(mse_list), np.mean(margin_of_error_list)

def train_lgbm(data, cross_validation=False, chunks=5, validation_size=45, cv_offset_list = [30, 60, 90, 120], params=None):
    train_data_day = data.copy()
    mse_list = []
    margin_of_error_list = []
    
    assert chunks <= len(cv_offset_list), f'Not enough periouds in offset list, chunks should be less or equal {len(cv_offset_list)=}'
    cv_offset_list = cv_offset_list[:chunks]

    if cross_validation:
        for cv_offset in cv_offset_list:
            train_data_day = data[:-cv_offset].copy()
            X_train, X_test, y_day_train, y_day_test = get_train_test_data(train_data=train_data_day, test_size=validation_size)
            mse, y_pred, model = train_default_LGBMRegressor(X_train, X_test, y_day_train, y_day_test, params=params)
            lower_bound, upper_bound, margin_of_error = calculate_confidence_inteval(y_pred=y_pred, y_true=y_day_test)
            margin_of_error_list.append(margin_of_error)
            mse_list.append(mse)
    else:
        X_train, X_test, y_day_train, y_day_test = get_train_test_data(train_data=train_data_day, test_size=validation_size)
        mse, y_pred, model = train_default_LGBMRegressor(X_train, X_test, y_day_train, y_day_test, params=params)
        lower_bound, upper_bound, margin_of_error = calculate_confidence_inteval(y_pred=y_pred, y_true=y_day_test)
        margin_of_error_list.append(margin_of_error)
        mse_list.append(mse)

    return np.mean(mse_list), np.mean(margin_of_error_list)

def train_catboost(data, cross_validation=False, chunks=5, validation_size=45, cv_offset_list = [30, 60, 90, 120], params=None):
    train_data_day = data.copy()
    mse_list = []
    margin_of_error_list = []
    
    assert chunks <= len(cv_offset_list), f'Not enough periouds in offset list, chunks should be less or equal {len(cv_offset_list)=}'
    cv_offset_list = cv_offset_list[:chunks]

    if cross_validation:
        for cv_offset in cv_offset_list:
            train_data_day = data[:-cv_offset].copy()
            X_train, X_test, y_day_train, y_day_test = get_train_test_data(train_data=train_data_day, test_size=validation_size)
            mse, y_pred, model = train_default_CatBoost(X_train, X_test, y_day_train, y_day_test, params=params)
            lower_bound, upper_bound, margin_of_error = calculate_confidence_inteval(y_pred=y_pred, y_true=y_day_test)
            margin_of_error_list.append(margin_of_error)
            mse_list.append(mse)
    else:
        X_train, X_test, y_day_train, y_day_test = get_train_test_data(train_data=train_data_day, test_size=validation_size)
        mse, y_pred, model = train_default_CatBoost(X_train, X_test, y_day_train, y_day_test, params=params)
        lower_bound, upper_bound, margin_of_error = calculate_confidence_inteval(y_pred=y_pred, y_true=y_day_test)
        margin_of_error_list.append(margin_of_error)
        mse_list.append(mse)

    return np.mean(mse_list), np.mean(margin_of_error_list)

def generate_binary_combinations(num_digits):
    """
    Генерирует все возможные комбинации двоичных цифр заданной длины.
    """
    for i in range(2**num_digits):
        yield list(format(i, f"0{num_digits}b"))

def create_example_data_with_features(df, selected_functions: list, feature_test_size = 'min'):
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

    features_dict = min_features_dict if feature_test_size == 'min' else all_features_dict

    for i, key in enumerate(selected_functions):
        if key == '1':
            use_features.append(features_dict[i].__name__)
            features_dict[i]()
          
    features_class.merge_features()
    
    return features_class.df_with_features, use_features, features_class.params_count

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

def select_top_model_vec(model_result_table, top_mse = 3, top_fit_time = 1):
    top_models = model_result_table.sort_values(by='MSE', ascending=True).head(top_mse).sort_values(by='fit_time', ascending=True).loc[:top_fit_time,:]
    selected_combinations = []
    for row in top_models.iloc[:,:-3].iterrows():
        selected_combinations.append(list(row[1]))
    #Take only 1 element. List and append for maybe more complex logic in model selection
    #------
    selected_combination = selected_combinations[0]
    #------
    selected_combination = [str(x) for x in selected_combination]
    comb_len = len(selected_combination)
    features_dict_size = 'min' if comb_len <= 4 else 'all'
   
    return selected_combination, features_dict_size



#----------------------------------------
#Results interpretation and visualization
#----------------------------------------

def compare_with_dummy_model(y_train, y_test, y_pred, model_mse):
    test_size = len(y_test)
    dummy_mse = sum((y_test - y_train.mean())**2) / len(y_test)
    dummy_mse2 = sum((y_test - y_train[len(y_train)-test_size*3:-test_size].mean())**2) / test_size
    model_is_ok = True

    if dummy_mse < model_mse:
        print('FIRST CHECK - MODEL IS GARBAGE')
        model_is_ok = False

    if dummy_mse2 < model_mse:
        print('SECOND CHECK - MODEL IS GARBAGE')
        model_is_ok = False

    if np.sum(y_pred < 0) > 0:
        print('MODEL HAVE MINUS REVENUE PREDICTIONS')
        model_is_ok = False
    
    if model_is_ok:
        print('MODEL IS OK')


def compare_trpred_periods(y_test, y_pred, periods=[7, 14, 30, 45, 60]):
    final_accuracy_mark = 0
    pred_size = len(y_pred)
    periods = [days for days in periods if days <= pred_size]
    
    for days in periods:
        sales_fact = sum(y_test[:days+1])
        sales_pred = sum(y_pred[:days+1])
        
        print(f'Revenue for last {days} days was {sales_fact:.2f}')
        print(f'Predicted revenue {sales_pred:.2f}')
        print(f'Difference: {sales_fact - sales_pred:.2f} {((sales_fact - sales_pred) / sales_fact)*100:.2f}%')
        print(f'----------------------')
        # if days > 15:
        #     final_accuracy_mark+=abs(((sales_fact - sales_pred) / sales_fact)*100)

    final_accuracy_mark = ((np.sum(y_test) - abs(np.sum(y_test) - np.sum(y_pred))) / np.sum(y_test))*100
    mean_accuracy = np.mean(((y_test - (np.abs(y_test - y_pred))) / y_test)*100)
    print('#####')
    print('#####')
    print(f'Total fact sales = {np.sum(y_test)}')
    print(f'Total pred sales = {np.sum(y_pred)}')
    print(f'Total fact sales minus total pred sales = {(np.sum(y_test) - np.sum(y_pred)):.2f}')
    print(f'Total Accuracy score: {final_accuracy_mark:.2f}%')
    print(f'Mean accuracy (on each point) {mean_accuracy:.2f}%')
    print(f'----------------------')
    return final_accuracy_mark, mean_accuracy


def plot_predictions(y_pred, y_test, lower_bound=None, upper_bound=None):
    y_day_pred_series = pd.Series(y_pred, index=y_test.index)

    # Создайте график и добавьте оба DataSeries на него
    plt.figure(figsize=(10, 6))
    plt.plot(y_test.index, y_test.values, label='y_day_test', marker='o', color='b', linestyle='-')
    plt.plot(y_day_pred_series.index, y_day_pred_series.values, label='y_day_pred', marker='x', color='r', linestyle='-')
    
    if lower_bound is not None and upper_bound is not None:
        plt.fill_between(y_day_pred_series.index, lower_bound, upper_bound, color='red', alpha=0.5)

    # Добавьте легенду графика
    plt.legend()

    # Настройте заголовок и подписи осей
    plt.title('График значений y_day_test и y_day_pred')
    plt.xlabel('Индекс')
    plt.ylabel('Значение')

    # Отобразите график
    plt.show()
    if lower_bound is not None and upper_bound is not None:
        sum_lower = sum(lower_bound > y_test)
        sum_upper = sum(upper_bound < y_test)
        total_miss = sum_lower + sum_upper
        total_points = len(y_test)
        correct_points = total_points - total_miss
        print(f'Фактические продажи ниже lower_bound {sum_lower}, {(sum_lower / total_points)*100:.2f}%')
        print(f'Фактические продажи выше upper_bound {sum_upper}, {(sum_upper / total_points)*100:.2f}%')
        print(f'Фактические продажи в рамках границ прогнозов {correct_points}, {(correct_points / total_points)*100:.2f}%')


def plot_differences_in_predictions(y_pred, y_test, margin_of_error=None):
    y_day_pred_series = pd.Series(y_pred, index=np.arange(0, len(y_test)))
    fig, axs = plt.subplots(2, figsize=(10,8))
    axs[0].plot(y_day_pred_series.index, (y_test - y_day_pred_series.values), label='difference', color='b', linestyle='-', marker='x')
    axs[1].plot(y_day_pred_series.index, ((y_test - y_day_pred_series.values) / y_test)*100, label='difference %', color='r', linestyle='-', marker='o')
    axs[1].hlines(-50, 0, len(y_test), linestyles='--', label='-50%')
    axs[1].hlines(50, 0, len(y_test), linestyles='--', label='+50%')
    axs[1].hlines(-100, 0, len(y_test), linestyles='--', label='-100%')
    axs[1].hlines(100, 0, len(y_test), linestyles='--', label='+100%')

    if margin_of_error is None:
        axs[0].hlines(-100000, 0, len(y_test), linestyles='--', label='-100k', color='g')
        axs[0].hlines(100000, 0, len(y_test), linestyles='--', label='+100k', color='g')
    else:
        axs[0].hlines(-margin_of_error, 0, len(y_test), linestyles='--', label=f'-{margin_of_error/ 1000:.0f}k moe', color='g')
        axs[0].hlines(margin_of_error, 0, len(y_test), linestyles='--', label=f'+{margin_of_error/ 1000:.0f}k moe', color='g')

    axs[0].hlines(-500000, 0, len(y_test), linestyles='--', label='-500k', color='r')
    axs[0].hlines(500000, 0, len(y_test), linestyles='--', label='+500k', color='r')

    axs[0].legend()
    axs[1].legend()
    plt.plot

def count_points_diff(y_test, y_pred, points = [5, 10, 15, 25, 50, 75, 100, 200]):
    y_day_pred_series = pd.Series(y_pred, index=y_test.index)
    diff = abs((y_test - y_day_pred_series.values) / y_test)*100
    print(f'Всего точек для прогноза {len(y_test)}')
    for threshold in points:
        sum_dif = sum(diff > threshold)
        print(f'В результатах прогноза {sum_dif} точек имеют разницу с фактов более {threshold}%')

def calculate_low_up_bounds(y_pred, margin_of_error, y_true_index):
    lower_bound = pd.Series(y_pred - margin_of_error)
    lower_bound.index = y_true_index
    upper_bound = pd.Series(y_pred + margin_of_error)
    upper_bound.index = y_true_index
    return lower_bound, upper_bound


def calculate_confidence_inteval(y_pred, y_true):
    # Остатки
    residuals = y_pred - y_true

    # Стандартное отклонение остатков
    std_residuals = np.std(residuals)

    # Доверительный интервал (95%)
    n = len(residuals)
    t_value = t.ppf(0.99, df=n-1)
    margin_of_error = t_value * std_residuals / np.sqrt(n)

    # Доверительный интервал для прогнозов
    lower_bound, upper_bound = calculate_low_up_bounds(y_pred, margin_of_error, y_true.index)
    return lower_bound, upper_bound, margin_of_error