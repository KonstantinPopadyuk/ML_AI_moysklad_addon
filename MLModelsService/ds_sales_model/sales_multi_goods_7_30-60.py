# %%
import warnings
warnings.filterwarnings('ignore')

# %%
import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import pickle

# %%
from ds_sales_modules import SalesModelData
from ds_sales_modules import TreeBoostedSalesModel
from ds_sales_modules import (XGboostStrategy)
from ds_sales_modules import LoggerModelsResults
from ds_sales_modules import GoodsPredictStrategy

# %%
VALIDATION_SIZE = 15+1
TEST_SIZE = 15
GAP = 1
# CROSVAL_LIST = [TEST_SIZE+GAP, TEST_SIZE+30+GAP, TEST_SIZE+60+GAP, TEST_SIZE+90+GAP]
CROSVAL_LIST = [TEST_SIZE+GAP, TEST_SIZE+30+GAP]
CHUNKS = len(CROSVAL_LIST)
FEATURES_BLOCKS_QUANTITY_XGBOOST = 2 #cant be more then 2
OPTUNA_TRIALS_XGBOOST = 10
ROLLING_WINDOW = [7, 30, 60]

models_results_logs = LoggerModelsResults()

# %%
df = SalesModelData()
df = df.get_data(period=True, translit=True, left_lim='2023-01-01', right_lim='2024-12-31')
print(f'df size: rows {len(df)} columns {len(df.columns)}')

# %%
xgboost_model = TreeBoostedSalesModel(df=df,
                                      model_strategy=XGboostStrategy(),
                                      train_test_split_strategy=GoodsPredictStrategy(df=df, rolling_windows=ROLLING_WINDOW), 
                                      num_features_blocks=FEATURES_BLOCKS_QUANTITY_XGBOOST,
                                      logs=models_results_logs)

# %%
#hot-fix, need to refactor later
#--------
xgboost_model.feature_test_size = 'goods_model'
#--------

xgboost_model.main_loop_with_cv(chunks=CHUNKS,
                                validation_size=VALIDATION_SIZE,
                                cv_offset_list=CROSVAL_LIST)

# %%
xgboost_model.set_results_table()
xgboost_model.models_results.head(10)

# %%
xgboost_model.select_top_model_vec(top_mse = 3, top_fit_time = 1)
xgboost_model.selected_model_combination

# %%
#In this model it is to long step for only reason to know default_mse
#also it is strangly long in comparison with .get_best_model_pred_on_test(). need to check
# mse_day, _, _ = xgboost_model._train_tree(data=xgboost_model.selected_data_for_best_model, 
#                                           cross_validation=False, 
#                                           logs=False, 
#                                           validation_size=TEST_SIZE+1, 
#                                           params=None)
# print(f'MSE default_XGBRegressor day prediction: {mse_day}')

# %%
# xgboost_model._manually_set_top_model_vec(['1'])
# xgboost_model._manually_set_top_model_vec(['0'])
# xgboost_model._manually_set_top_model_vec(['0', '0', '0', '0', '1', '1', '0'])
# xgboost_model._manually_set_top_model_vec(['0', '0', '1', '0', '1', '1', '0'])

# %%
xgboost_model.selected_data_for_best_model

# %%
best_params = xgboost_model.start_optuna(data=xgboost_model.selected_data_for_best_model, n_trials=OPTUNA_TRIALS_XGBOOST)

# %%
y_train, y_test, y_pred, mse = xgboost_model.get_best_model_pred_on_test(test_size=TEST_SIZE+1)

# %%
fi = pd.DataFrame(data=xgboost_model.best_cv_model.feature_importances_, index=xgboost_model.best_cv_model.feature_names_in_, columns=['Importances'])
fi.sort_values('Importances', ascending=True)[-20:].plot(kind='barh')

# %%
_, margin_of_error = xgboost_model._train_tree(data=xgboost_model.selected_data_for_best_model, 
                                               cross_validation=True, 
                                               chunks=CHUNKS, 
                                               validation_size=VALIDATION_SIZE, 
                                               cv_offset_list = CROSVAL_LIST, 
                                               params=best_params)
lower_bound, upper_bound = xgboost_model.calculate_low_up_bounds(y_pred, margin_of_error, y_test.index)

# %%
margin_of_error

# %%
models_results_logs.all_models_parametrs

# %% [markdown]
# Save model
# ----------

# %%

file_name = "sales_multi_goods_7_30-60.pkl"

# save
pickle.dump(xgboost_model.best_cv_model, open(file_name, "wb"))

# %% [markdown]
# Save predictions
# --------
# 

# %%
xgboost_model._predict_on_last_period(), len(xgboost_model._predict_on_last_period()[0])

# %%
preds = pd.DataFrame(columns=y_train.columns, data=xgboost_model._predict_on_last_period())
preds

# %%
file_name_prediction = "sales_multi_goods_7_30-60_predictions.pkl"
preds = pd.DataFrame(columns=y_train.columns, data=xgboost_model._predict_on_last_period())

# %%
preds_7 = preds.iloc[:, preds.columns.str.contains('7_days')]
preds_7 = preds_7.T
preds_7.columns = ['7_preds']
preds_7.index = preds_7.index.str.replace(r'_\d+_sum_\d+_days$', '', regex=True)

preds_30 = preds.iloc[:, preds.columns.str.contains('30_days')]
preds_30 = preds_30.T
preds_30.columns = ['30_preds']
preds_30.index = preds_30.index.str.replace(r'_\d+_sum_\d+_days$', '', regex=True)

preds_60 = preds.iloc[:, preds.columns.str.contains('60_days')]
preds_60 = preds_60.T
preds_60.columns = ['60_preds']
preds_60.index = preds_60.index.str.replace(r'_\d+_sum_\d+_days$', '', regex=True)

# %%
# preds_all = pd.concat([preds_7, preds_30, preds_60], axis=0)
preds_all = pd.concat([preds_7, preds_30, preds_60], axis=1)

# %%
preds_all

# %%
preds_all.to_pickle(file_name_prediction)


