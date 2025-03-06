import pandas as pd

import sys
import os
# Add the root project directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from transformed_data import ProcessedData 

class SalesModelData():
    def __init__(self):
        self._raw_df = ProcessedData().df 

    def get_data(self, period: bool, translit=False, left_lim='2023-01-01', right_lim='2023-12-31'):
        return self._load_data(period, translit, left_lim, right_lim)

    def _load_data(self, limited_period=True, translit=False, left_lim='2023-01-01', right_lim='2023-12-31'):
        df = self._raw_df
        df.created_day = pd.to_datetime(df.created_day)

        df = df.sort_values(by='created', ascending=True)
        if limited_period:
            df = df[df.created_day >= pd.Timestamp(left_lim)]
            df = df[df.created_day <= pd.Timestamp(right_lim)]
            
        
        df = df[df.state != 'Возврат']
        if translit:
            df.columns = [SalesModelData.translit_column_name(column) for column in df.columns]

        #changing companyType (have diceded that client can't be individual if he has large orders, probably there is a mistake in data source)
        not_individual = df.groupby(['created_day', 'agent_name', 'companyType']).agg({'sum':'sum'}).reset_index().query('sum > 50000 and companyType == "individual"').copy()
        list_not_individual = not_individual['agent_name'].unique()
        df.loc[df['agent_name'].isin(list_not_individual), 'companyType'] = 'legal'
        #replace enterprenuer for legal
        df['companyType'] = df['companyType'].replace('entrepreneur', 'legal')

        df['day'] = df['created_day'].dt.day

        return df
    
    @staticmethod
    def translit_column_name(col_name):
        translit_dict = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
            'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
            'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
            'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '',
            'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', 
            ' ':'_', '"':'', ',':'','[':'',']':'', '{':'', '}':'', ':':''
        }

        translit_name = ''
        for char in col_name:
            if char.lower() in translit_dict:
                if char.islower():
                    translit_name += translit_dict[char]
                else:
                    translit_name += translit_dict[char.lower()].capitalize()
            else:
                translit_name += char
        return translit_name
    
    @staticmethod
    def reverse_translit_column_name(col_name):

        reverse_translit_dict = {
            'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д', 'e': 'е', 'yo': 'ё',
            'zh': 'ж', 'z': 'з', 'i': 'и', 'y': 'й', 'k': 'к', 'l': 'л', 'm': 'м',
            'n': 'н', 'o': 'о', 'p': 'п', 'r': 'р', 's': 'с', 't': 'т', 'u': 'у',
            'f': 'ф', 'h': 'х', 'ts': 'ц', 'ch': 'ч', 'sh': 'ш', 'sch': 'щ',
            'y': 'ы', 'yu': 'ю', 'ya': 'я'}

        reversed_name = ''
        i = 0
        while i < len(col_name):
            char = col_name[i]
            if char.isupper():
                char = char.lower()
            if i + 1 < len(col_name) and col_name[i:i+2] in reverse_translit_dict:
                reversed_name += reverse_translit_dict[col_name[i:i+2]]
                i += 2
            elif char in reverse_translit_dict:
                reversed_name += reverse_translit_dict[char]
                i += 1
            else:
                reversed_name += char
                i += 1

        return reversed_name