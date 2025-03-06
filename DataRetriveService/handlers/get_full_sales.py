from .decorators import *

import requests
import json
import pandas as pd
from urllib.parse import urlparse

from settings import settings



@retry_request_decorator
def _get_all_sales_request():
    headers = {
        'Accept-Encoding': 'gzip',
        'Authorization': settings.MOYSKLAD_TOKEN
        }
    all_orders = []
    offset = 0
    max_limit = 1000
    i=0
    print('START GATHERING ORDERS DATA')
    while True:
        params = {"limit": max_limit, "offset": offset}
        res = requests.get('https://api.moysklad.ru/api/remap/1.2/entity/customerorder', headers=headers, params=params)
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
    
    print('END OF WHILE LOOP')
    df = pd.DataFrame.from_dict(all_orders)
    useful_columns = [
        'id', 'agent', 'updated', 'name', 'moment', 'sum', 'state', 'created', 'positions', 
        'vatSum', 'payedSum', 'shippedSum', 'invoicedSum', 'reservedSum',  'shipmentAddress', 'shipmentAddressFull'
    ]

    df = df[useful_columns]
    df = df.rename(columns={'id':'order_id'})

    print('END OF FIRST FUNCTION')
    return df


def get_sales_data():

    # Get all data
    df = _get_all_sales_request()

    ## Modify data
    print('START MODIFYING DATA')
    steps = 7
    # Change state, position and agent fields
    df.state = df.state.apply(lambda x: x['meta']['href'])
    df.positions = df.positions.apply(lambda x: x['meta']['href'])
    df.agent = df.agent.apply(lambda x: x['meta']['href'])

    print(f'#1/{steps} Change state, position and agent fields COMPLETED')
    
    # Change address data
    def try_extract_city(addres):
        try:
            return addres['city']
        except:
            return 'Город не указан'
        
    df.shipmentAddressFull = df.shipmentAddressFull.apply(try_extract_city)
    df = df.rename(columns={'shipmentAddressFull':'city'})
    df.shipmentAddress = df.shipmentAddress.fillna('Адрес доставки не указан')

    print(f'#2/{steps} Change address data COMPLETED')

    # #Collect and exlode positions in each order
    # @retry_request_decorator
    # def _get_json_request(x):
    #     headers = {'Accept-Encoding': 'gzip', 'Authorization': settings.TOKEN}
    #     res = requests.get(x, headers=headers)
    #     res = json.loads(res.text)
    #     return res
        
 
    # df.positions = df.positions.apply(lambda x: _get_json_request(x)['rows'])

    # print(f'#3/{steps} Collect and exlode positions in each order COMPLETED')

    # Collect and explode positions in each order
    @retry_request_decorator
    def _get_json_request(x):
        headers = {'Accept-Encoding': 'gzip', 'Authorization': settings.MOYSKLAD_TOKEN}
        res = requests.get(x, headers=headers)
        res = json.loads(res.text)
        return res  # Return the entire JSON response


    # Use ThreadPoolExecutor for parallel processing
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    print(f'#3/{steps} Starting parallel collection of order positions...')
    with ThreadPoolExecutor(max_workers=100) as executor:
        # Create a dictionary to maintain order
        future_to_url = {executor.submit(_get_json_request, url): i 
                        for i, url in enumerate(df.positions)}
        
        # Collect results in order
        results = [None] * len(df.positions)
        print(f'{len(future_to_url)=}')
        for future in as_completed(future_to_url):
            index = future_to_url[future]
            try:
                # Access 'rows' here after ensuring the request was successful
                response = future.result()
                results[index] = response.get('rows', [])
            except Exception as e:
                print(f'Error processing request {index}: {str(e)}')
                results[index] = []
    
    df.positions = results
    print(f'#3/{steps} Collect and explode positions in each order COMPLETED')


    # Change object data quantity, price and assortment
    @tryexcept_decorator
    def _extract_values(row, keys):
        return {key: row.get(key) for key in keys}   

    keys_to_extract = ['quantity', 'price', 'assortment']

    df = df.explode('positions')
    df = df.loc[df.positions.notna()]
    df = pd.concat([df.drop(['positions'], axis=1), df['positions'].apply(lambda x: pd.Series(_extract_values(x, keys_to_extract)))], axis=1)
    df = df.loc[df.assortment != 'empty']

    df.assortment = df.assortment.apply(lambda x: x['meta']['href'])

    print(f'#4/{steps} Change object data quantity, price and assortment COMPLETED')


    # Extracting ids from urls for
    @tryexcept_decorator
    def _extract_end_of_url(url_string):
        parsed_url = urlparse(url_string)
        path_parts = parsed_url.path.split('/')
        return path_parts[-1]

    df['assortment_id'] = df.assortment.apply(_extract_end_of_url)
    df['agent'] = df.agent.apply(_extract_end_of_url)
    df = df.rename(columns={'agent':'agent_id'})

    print(f'#5/{steps} Extracting ids from urls for COMPLETED')

    # Exctrat all state names
    df.state = df.state.apply(_extract_end_of_url)

    all_unique_states = df.state.unique().tolist()

    @retry_request_decorator
    def _get_map_state_names(all_states):
        headers = {
            'Accept-Encoding': 'gzip',
            'Authorization': settings.MOYSKLAD_TOKEN
            }

        url = 'https://api.moysklad.ru/api/remap/1.2/entity/customerorder/metadata/states/'
        state_dict = {}

        for state in all_states:
            res = requests.get(url+state, headers=headers)
            state_dict[state] = json.loads(res.text)['name']

        return state_dict
    
    df.state = df.state.replace(_get_map_state_names(all_unique_states))

    print(f'#6/{steps} Extracting state names COMPLETED')

    
    # In this case order do not matter - will use in another part of programm later
    columns_order = ['order_id', 'agent_id', 'name', 'updated',  'moment', 'created', 'state', 'sum',  
        'vatSum', 'payedSum', 'shippedSum', 'invoicedSum', 'reservedSum',
        'assortment_id', 'quantity', 'price', 'shipmentAddress', 'city']

    df = df[columns_order]

    # For optimisation purposes it is not correct to /100 but db is small, so maby change this part later
    int_colums = ['sum', 'vatSum', 'payedSum', 'shippedSum', 'invoicedSum', 'reservedSum', 'price']
    
    df[int_colums] = df[int_colums] / 100
    df[int_colums] = df[int_colums].fillna(0.0)

    # Confirm that datetime is datetime
    datetime_columns = ['updated',  'moment', 'created']
    for column in datetime_columns:
        df[column] = pd.to_datetime(df[column], format='%Y-%m-%d %H:%M:%S.%f')
    
    print(f'#7/{steps} Confirm that datetime is datetime COMPLETED')
    print('-------------------')
    print('ALL STEPS COMPLETED')
    return df.to_dict(orient='records')


