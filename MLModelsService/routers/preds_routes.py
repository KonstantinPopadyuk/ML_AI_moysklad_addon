from fastapi import APIRouter
from .rediscachewrapper import cache_response
from datetime import timedelta
from transformed_data import SalesPredsData, SalesStockReports

preds_router = APIRouter()
default_ttl_min_time = 60*24

@preds_router.get("/create_stock_preds")
@cache_response(key_prefix="stock_preds", ttl=timedelta(minutes=default_ttl_min_time))
async def create_stock_preds():
    stock_preds = SalesStockReports(df=SalesPredsData())
    response = stock_preds.get_full_table()
    return response.to_dict(orient='records')

@preds_router.get("/create_stock_days_preds/{n}")
@cache_response(key_prefix="stock_days_preds_{n}", ttl=timedelta(minutes=default_ttl_min_time))
async def create_stock_preds(n: str = '30'):
    stock_preds = SalesStockReports(df=SalesPredsData())
    response = stock_preds.get_N_days_need_to_buy_report(n=int(n))
    return response.to_dict(orient='records')