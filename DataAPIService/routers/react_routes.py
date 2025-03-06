from datetime import timedelta
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
from .rediscachewrapper import cache_response, redis_client
import requests
import json


react_router = APIRouter(prefix='/react_data')
ML_SERVICE_URL = 'http://ml_models:8010'
default_ttl_min_time = 60*24

@react_router.get('/agents_type_grid')
@cache_response(key_prefix="agents_type_grid", ttl=timedelta(minutes=default_ttl_min_time))
async def get_agents_type_data(time_period: str = 'month') -> List[Dict[str, Any]]:
    """
    Retrieve aggregated sales data grouped by company type.
    
    Parameters:
    - time_period (str): Time period for analysis ('day', 'week', 'month', 'year')
    
    Returns:
    - Dictionary containing:
        - companyType: Type of company
        - orders_count: Number of orders
        - orders_total_sum: Total sales amount
        - average_order_value: Average value per order
    """
    data = json.loads(requests.get(f"{ML_SERVICE_URL}/get_agents_type_report?time_period={time_period}").text)
    return data

@react_router.get('/agents_name_grid')
@cache_response(key_prefix="agents_name_grid", ttl=timedelta(minutes=default_ttl_min_time))
async def get_agents_name_data(time_period: str = 'month') -> List[Dict[str, Any]]:
    """
    Retrieve sales data aggregated by individual agents/customers.
    
    Parameters:
    - time_period (str): Time period for analysis ('day', 'week', 'month', 'year')
    
    Returns:
    - Dictionary containing:
        - agent_name: Name of the agent/customer
        - orders_count: Number of orders
        - orders_total_sum: Total sales amount
        - average_order_value: Average value per order
    """
    data = json.loads(requests.get(f"{ML_SERVICE_URL}/get_agents_name_data?time_period={time_period}").text)
    return data

@react_router.get('/item_type_grid')
@cache_response(key_prefix="item_type_grid", ttl=timedelta(minutes=default_ttl_min_time))
async def get_item_type_data(time_period: str = 'month') -> List[Dict[str, Any]]:
    """
    Retrieve sales data aggregated by product categories.
    
    Parameters:
    - time_period (str): Time period for analysis ('day', 'week', 'month', 'year')
    
    Returns:
    - Dictionary containing:
        - item_type: Product category
        - orders_count: Number of orders
        - orders_total_sum: Total sales amount
        - average_order_value: Average value per order
    """
    data = json.loads(requests.get(f"{ML_SERVICE_URL}/get_item_type_data?time_period={time_period}").text)
    return data

@react_router.get('/volume_type_grid')
@cache_response(key_prefix="volume_type_grid", ttl=timedelta(minutes=default_ttl_min_time))
async def get_volumes_data(time_period: str = 'month') -> List[Dict[str, Any]]:
    """
    Retrieve sales data aggregated by product volumes.
    
    Parameters:
    - time_period (str): Time period for analysis ('day', 'week', 'month', 'year')
    
    Returns:
    - Dictionary containing:
        - volume_ml: Product volume in milliliters
        - orders_count: Number of orders
        - orders_total_sum: Total sales amount
        - average_order_value: Average value per order
    """
    data = json.loads(requests.get(f"{ML_SERVICE_URL}/get_volumes_data?time_period={time_period}").text)
    return data

@react_router.get('/city_grid')
@cache_response(key_prefix="city_grid", ttl=timedelta(minutes=default_ttl_min_time))
async def get_city_data(time_period: str = 'month') -> List[Dict[str, Any]]:
    """
    Retrieve sales data aggregated by cities.
    
    Parameters:
    - time_period (str): Time period for analysis ('day', 'week', 'month', 'year')
    
    Returns:
    - Dictionary containing:
        - city: City name
        - orders_count: Number of orders
        - orders_total_sum: Total sales amount
        - average_order_value: Average value per order
    """
    data = json.loads(requests.get(f"{ML_SERVICE_URL}/get_city_data?time_period={time_period}").text)
    return data

@react_router.get('/preds/stock')
@cache_response(key_prefix="preds/stock", ttl=timedelta(minutes=default_ttl_min_time))
async def get_react_data():
    data = json.loads(requests.get(f"{ML_SERVICE_URL}/create_stock_preds").text)
    return data

@react_router.get('/preds/stock_days/{n}')
@cache_response(key_prefix="preds/stock_days/{n}", ttl=timedelta(minutes=default_ttl_min_time))
async def get_react_data(n: str):
    data = json.loads(requests.get(f"{ML_SERVICE_URL}/create_stock_days_preds/{n}").text)
    return data

@react_router.delete('/cache/clear')
async def clear_cache():
    redis_client.flushdb()
    return {"message": "Cache cleared successfully"}