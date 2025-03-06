import pandas as pd

class LoggerModelsResults:
    def __init__(self) -> None:
        self.all_models_parametrs = pd.DataFrame()

    def update(self, index, param, result):
        if index not in self.all_models_parametrs.index:
            new_index = self.all_models_parametrs.index.union([index])
            self.all_models_parametrs = self.all_models_parametrs.reindex(index=new_index)
            
        if param not in self.all_models_parametrs.columns:
            new_columns = self.all_models_parametrs.columns.union([param])
            self.all_models_parametrs = self.all_models_parametrs.reindex(columns=new_columns)
            
        self.all_models_parametrs.loc[index, param] = result


