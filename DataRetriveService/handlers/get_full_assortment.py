import requests
import json
import pandas as pd

from settings import settings
from fastapi import HTTPException

def _get_assortment_request():
    headers = {
        'Accept-Encoding': 'gzip',
        'Authorization': settings.MOYSKLAD_TOKEN
        }
    all_assortment = []
    offset = 0
    max_limit = 1000

    while True:
        params = {"limit": max_limit, "offset": offset, "filter": 'archived=true;archived=false'}
        res = requests.get('https://api.moysklad.ru/api/remap/1.2/entity/assortment', headers=headers, params=params)

        if res.status_code != 200:
            raise HTTPException(
                status_code=res.status_code,
                detail=f"API Error: {res.text}"
            )
        
        res = json.loads(res.text)['rows']
        
        all_assortment.extend(res)
        offset = offset + max_limit

        if len(res) < max_limit:
           break

    short_dict_keys = [
        'id', 'updated', 'name', 'description', 'code', 'archived', 
        'pathName', 'salePrices', 'paymentItemType', 'volume', 
        'variantsCount', 'stock', 'reserve', 'inTransit', 'quantity'
        ]

    df = pd.DataFrame.from_dict(all_assortment)[short_dict_keys]

    return df


def get_assorment_data():

    # Get all assortment data
    df = _get_assortment_request()

    ## Modify data

    # This part iter through each row and make new dataframe with prices
    # Then concates it with original table
    # Looks horrible, need to rewrite in more eleghant way

    def _take_prices(data):
        """
            take column and parse all prices that json contains to one row
        """
        return pd.json_normalize(data)[['value', 'priceType.name']] \
                .pivot_table(columns='priceType.name', aggfunc=lambda x: x/100) \
                .reset_index(drop=True)

    new_df = pd.DataFrame()
    for _, row in df.iterrows():
        new_df = pd.concat([new_df, _take_prices(row['salePrices'])])
    new_df.columns.name = None
    new_df.reset_index(inplace=True, drop=True)

    final_df = pd.concat([df, new_df], axis=1)
    final_df.drop(['salePrices'], axis=1, inplace=True)


    # Rename some columns
    price_map = {'Цена $':'price_usd',
                'Цена Дистр':'price_distr', 
                'Цена ОПТ':'price_opt', 
                'Цена Производство':'price_proiz', 
                'Цена РРЦ':'price_rrz',
                'Цена Сайт':'price_site', 
                'Цена Тех':'price_tech'
                }
    
    

    final_df = final_df.rename(columns=price_map)
    final_df.columns = final_df.columns.str.lower()
    final_df.description = final_df.description.fillna('Описание не указано')

    final_df.updated = pd.to_datetime(final_df.updated, format='%Y-%m-%d %H:%M:%S.%f')

    
    return final_df.to_dict(orient='records')



