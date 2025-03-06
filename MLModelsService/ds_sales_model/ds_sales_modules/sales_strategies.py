from abc import ABC, abstractmethod

from xgboost import XGBRegressor
from catboost import CatBoostRegressor, Pool
from lightgbm import LGBMRegressor
from lightgbm import early_stopping
from sklearn.metrics import mean_squared_error


class ModelStrategy(ABC):
    @abstractmethod
    def get_algorithm(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_optuna_objective(self):
        pass    


class XGboostStrategy(ModelStrategy):
    def get_algorithm(self):
        return self.train_default_XGBRegressor
    
    def get_name(self):
        return 'XGBoost'
    
    def get_optuna_objective(self):
        def objective(trial, data, train_alg, chunks, validation_size, cv_offset_list):
            params = {
                'max_depth': trial.suggest_int('max_depth', 2, 9),
                'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
                'n_estimators': trial.suggest_int('n_estimators', 10, 200),
                'gamma': trial.suggest_float('gamma', 0, 0.2),
                'subsample': trial.suggest_float('subsample', 0.8, 1.0),
                'colsample_bytree': trial.suggest_float('colsample_bytree', 0.8, 1.0),
                'reg_alpha': trial.suggest_float('reg_alpha', 0, 0.5),
                'reg_lambda': trial.suggest_float('reg_lambda', 0, 1.0)
            }

            mse, _ = train_alg(data, cross_validation=True, chunks=chunks, validation_size=validation_size, cv_offset_list=cv_offset_list, params=params)
            return -mse 
        return objective
    
    @staticmethod
    def train_default_XGBRegressor(X_train, X_test, y_train, y_test, params=None):
        if params is None:
            model = XGBRegressor(early_stopping_rounds=50)
        else:
            model = XGBRegressor(**params, early_stopping_rounds=50)

        model.fit(X_train, y_train, eval_set=[(X_train, y_train),(X_test, y_test)], verbose=False)

        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)

        return mse, y_pred, model


class LGBMStrategy(ModelStrategy):
    def get_algorithm(self):
        return self.train_default_LGBMRegressor
    
    def get_name(self):
        return 'LGBM'
    
    def get_optuna_objective(self):
        def objective(trial, data, train_alg, chunks, validation_size, cv_offset_list):
            params = {
                "n_estimators": trial.suggest_int("n_estimators", 50, 1000),
                "learning_rate": trial.suggest_float("learning_rate", 1e-3, 1e-1, log=True),
                "num_leaves": trial.suggest_int("num_leaves", 3, 255),
                "max_depth": trial.suggest_int("max_depth", 3, 8),
                "min_child_samples": trial.suggest_int("min_child_samples", 5, 100),
                "subsample": trial.suggest_float("subsample", 0.5, 1.0),
                "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
                "reg_alpha": trial.suggest_float("reg_alpha", 1e-8, 10.0, log=True),
                "reg_lambda": trial.suggest_float("reg_lambda", 1e-8, 10.0, log=True),
            }

            mse, _ = train_alg(data, cross_validation=True, chunks=chunks, validation_size=validation_size, cv_offset_list=cv_offset_list, params=params)
            return -mse 
        return objective
    
    @staticmethod
    def train_default_LGBMRegressor(X_train, X_test, y_train, y_test, params=None):
        if params is None:
            model = LGBMRegressor(verbosity=-1)
        else:
            model = LGBMRegressor(**params, verbosity=-1)

        callbacks = [early_stopping(stopping_rounds=50, verbose=False)]
        model.fit(X_train, y_train, eval_set=[(X_test, y_test)], callbacks=callbacks)

        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)

        return mse, y_pred, model
    
class CatBoostStrategy(ModelStrategy):
    def get_algorithm(self):
        return self.train_default_CatBoost
    
    def get_name(self):
        return 'CatBoost'
    
    def get_optuna_objective(self):
        def objective(trial, data, train_alg, chunks, validation_size, cv_offset_list):
            params = {
                "iterations": trial.suggest_int("iterations", 100, 1000),
                "learning_rate": trial.suggest_float("learning_rate", 1e-3, 1e-1, log=True),
                "depth": trial.suggest_int("depth", 1, 10),
                "l2_leaf_reg": trial.suggest_float("l2_leaf_reg", 1e-8, 10.0, log=True),
                "random_strength": trial.suggest_float("random_strength", 1e-9, 10.0, log=True),
                "bagging_temperature": trial.suggest_float("bagging_temperature", 0.0, 1.0),
                "border_count": trial.suggest_int("border_count", 32, 255),
            }

            mse, _ = train_alg(data, cross_validation=True, chunks=chunks, validation_size=validation_size, cv_offset_list=cv_offset_list, params=params)
            return -mse 
        return objective
    
    @staticmethod
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