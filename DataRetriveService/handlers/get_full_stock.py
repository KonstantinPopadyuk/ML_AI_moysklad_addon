import requests
import json
import pandas as pd

from settings import settings
from fastapi import HTTPException

def _get_stock_request():
    headers = {
        'Accept-Encoding': 'gzip',
        'Authorization': settings.MOYSKLAD_TOKEN
        }
    all_stock = []
    offset = 0
    max_limit = 1000

    while True:
        params = {"limit": max_limit, "offset": offset, "groupBy": 'product', "filter": 'stockMode=all;quantityMode=all'}
        res = requests.get('https://api.moysklad.ru/api/remap/1.2/report/stock/all', headers=headers, params=params)
        if res.status_code != 200:
            raise HTTPException(
                status_code=res.status_code,
                detail=f"API Error: {res.text}"
            )
        res = json.loads(res.text)['rows']
        
        all_stock.extend(res)
        offset = offset + max_limit

        if len(res) < max_limit:
           break

    df = pd.DataFrame.from_dict(all_stock)

    df = df.drop(['meta','uom', 'externalCode', 'folder', 'price', 'salePrice', 'image'], axis=1)
    df = df[~df.name.str.contains('Занесение на')]

    return df


def get_stock_data():
    df = _get_stock_request()
    df.fillna('NaN', inplace=True)

    df = df.to_dict(orient='records')

    return df



