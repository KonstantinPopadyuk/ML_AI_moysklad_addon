from fastapi import FastAPI, APIRouter
import uvicorn
 
from datetime import timedelta
from routers import preds_router, reports_router, mlmodel_goods_router

app = FastAPI(title='ML Models Service')
default_ttl_min_time = 60*24

main_router = APIRouter()
main_router.include_router(reports_router, tags=['reports'])
main_router.include_router(preds_router, tags=['predictions'])
main_router.include_router(mlmodel_goods_router, tags=['ML models'])

@main_router.get('/')
async def healthy_check():
    return {'Hello':'Mr. Anderson'}

app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)