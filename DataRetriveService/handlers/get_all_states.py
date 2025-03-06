from settings import settings
import requests
import json

def get_map_state_names():
    #This was take from SQL script to database
    all_states = [
        '91e2111e-6bcf-11ed-0a80-07f7001fedc1',
        'a4aa7546-a873-11ed-0a80-0d0500113d80',
        'c62cb11b-b2c2-11ed-0a80-0cc40016a378',
        '2ee13d1a-953d-11ed-0a80-05ca0021343c',
        '83d32407-dd0b-11ed-0a80-10150078dbb5',
        'ca244491-ab8a-11ed-0a80-04fb003ac414',
        '91e21260-6bcf-11ed-0a80-07f7001fedc4',
        '2ec2779c-953d-11ed-0a80-05ca0021342c',
        '91e20f82-6bcf-11ed-0a80-07f7001fedbf',
        '2e73ce05-953d-11ed-0a80-05ca00213400',
        '91e21185-6bcf-11ed-0a80-07f7001fedc2',
        '91e211ca-6bcf-11ed-0a80-07f7001fedc3',
        '91e210bc-6bcf-11ed-0a80-07f7001fedc0',
        '91e212c4-6bcf-11ed-0a80-07f7001fedc5',
    ]

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