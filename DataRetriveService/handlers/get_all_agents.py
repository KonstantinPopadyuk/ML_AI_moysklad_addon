import requests
import json
import pandas as pd
from urllib.parse import urlparse

from settings import settings
from .decorators import *


@retry_request_decorator
def _get_all_agents_request():
    headers = {
        'Accept-Encoding': 'gzip',
        'Authorization': settings.MOYSKLAD_TOKEN
        }
    all_orders = []
    offset = 0
    max_limit = 1000
    i=0
    print('START GATHERING AGENTS DATA')
    while True:
        params = {"limit": max_limit, "offset": offset, "filter": 'archived=true;archived=false'}
        res = requests.get('https://api.moysklad.ru/api/remap/1.2/entity/counterparty', headers=headers, params=params)
        if res.status_code != 200:
            raise HTTPException(
                status_code=res.status_code,
                detail=f"API Error: {res.text}"
            )

        res = json.loads(res.text)['rows']

        all_orders.extend(res)
        offset = offset + max_limit

        i+=1
        print('____________________')
        print(f'------STEP {i}-------')
        print(f'{params=}')
        print(f'{len(res)=}')


        if len(res) < max_limit:
           break
        res = requests.get('https://api.moysklad.ru/api/remap/1.2/entity/organization', headers=headers, params=params)
        res = json.loads(res.text)['rows']

        all_orders.extend(res)


    print('END OF WHILE LOOP')


    df = pd.DataFrame.from_dict(all_orders)


    useful_columns = ['id', 'updated', 'name', 'created', 'companyType',
                      'actualAddress', 'phone', 'tags', 'legalTitle', 'legalLastName', 
                      'legalFirstName', 'email', 'legalAddress'
                      ]


    df = df[useful_columns]
    df = df.fillna('no data')

    print('END OF FIRST FUNCTION')
    return df


def get_all_agents_data():
    # Get all data
    df = _get_all_agents_request()

    ## Modify data
    print('START MODIFYING DATA')
    df = df.rename(columns={'id':'agent_id'})

    # Confirm that datetime is datetime
    datetime_columns = ['updated', 'created']
    for column in datetime_columns:
        df[column] = pd.to_datetime(df[column], format='%Y-%m-%d %H:%M:%S.%f')

    df.tags = df.tags.apply(lambda x: str(x))
    
    print('#1/1 Confirm that datetime is datetime COMPLETED')
    print('-------------------')
    print('ALL STEPS COMPLETED')
    print(df)

    return df.to_dict(orient='records')