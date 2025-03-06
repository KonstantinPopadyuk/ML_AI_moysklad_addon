from fastapi import APIRouter
from .rediscachewrapper import cache_response
from datetime import timedelta
from transformed_data import ProcessedData, Reports

reports_router = APIRouter()
default_ttl_min_time = 60*24

def init_reports_data() -> Reports:
    """
    Initializes the Reports object with processed data.
    
    Returns:
        Reports: An instance of the Reports class containing processed data.
    """
    return Reports(df=ProcessedData())

@reports_router.get("/get_agents_type_report")
@cache_response(key_prefix="agents_type_report", ttl=timedelta(minutes=default_ttl_min_time))
async def create_agents_type_report(time_period: str = 'month'):
    """
    Generates a report by customer type.
    
    Args:
        time_period (str): The time period for the report (default: 'month').
    
    Returns:
        List[Dict]: A list of dictionaries containing the report data with the following columns:
            - section_name: Customer type
            - num_products: Number of products
            - avg_product_price: Average product price
            - avg_order_price: Average order price
            - avg_order_amount: Average order amount
    """
    reports = init_reports_data()
    response = reports.get_agents_type_report(time_period)
    return response.to_dict(orient='records')

@reports_router.get('/get_agents_name_data')
@cache_response(key_prefix="agents_name_data", ttl=timedelta(minutes=default_ttl_min_time))
async def get_agents_name_data(time_period: str = 'month'):
    """
    Generates a report by customer name.
    
    Args:
        time_period (str): The time period for the report (default: 'month').
    
    Returns:
        List[Dict]: A list of dictionaries containing the report data with the following columns:
            - section_name: Customer name
            - num_products: Number of products
            - avg_product_price: Average product price
            - avg_order_price: Average order price
            - avg_order_amount: Average order amount
    """
    reports = init_reports_data()
    response = reports.get_agents_name_report(time_period)
    return response.to_dict(orient='records')

@reports_router.get('/get_item_type_data')
@cache_response(key_prefix="item_type_data", ttl=timedelta(minutes=default_ttl_min_time))
async def get_item_type_data(time_period: str = 'month'):
    """
    Generates a report by product type.
    
    Args:
        time_period (str): The time period for the report (default: 'month').
    
    Returns:
        List[Dict]: A list of dictionaries containing the report data with the following columns:
            - section_name: Product type
            - num_products: Number of products
            - avg_product_price: Average product price
            - avg_order_price: Average order price
            - avg_order_amount: Average order amount
    """
    reports = init_reports_data()
    response = reports.get_item_type_report(time_period)
    return response.to_dict(orient='records')

@reports_router.get('/get_volumes_data')
@cache_response(key_prefix="volumes_data", ttl=timedelta(minutes=default_ttl_min_time))
async def get_volumes_data(time_period: str = 'month'):
    """
    Generates a report by product volume.
    
    Args:
        time_period (str): The time period for the report (default: 'month').
    
    Returns:
        List[Dict]: A list of dictionaries containing the report data with the following columns:
            - section_name: Product volume
            - num_products: Number of products
            - avg_product_price: Average product price
            - avg_order_price: Average order price
            - avg_order_amount: Average order amount
    """
    reports = init_reports_data()
    response = reports.get_volumes_report(time_period)
    return response.to_dict(orient='records')

@reports_router.get('/get_city_data')
@cache_response(key_prefix="city_data_report", ttl=timedelta(minutes=default_ttl_min_time))
async def get_city_data(time_period: str = 'month'):
    """
    Generates a report by city name.
    
    Args:
        time_period (str): The time period for the report (default: 'month').
    
    Returns:
        List[Dict]: A list of dictionaries containing the report data with the following columns:
            - section_name: City name
            - num_products: Number of products
            - avg_product_price: Average product price
            - avg_order_price: Average order price
            - avg_order_amount: Average order amount
    """
    reports = init_reports_data()
    response = reports.get_city_report(time_period)
    return response.to_dict(orient='records')