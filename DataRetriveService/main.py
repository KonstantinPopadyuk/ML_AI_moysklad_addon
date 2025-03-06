from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from routers import *

from dotenv import load_dotenv


load_dotenv()
app = FastAPI(title='Data Retrieve App')

main_router = APIRouter()

# #routers that communicate with db
main_router.include_router(assortment_router, tags=['assortment'])
main_router.include_router(sales_router, tags=['sales'])
main_router.include_router(agents_router, tags=['agents'])
main_router.include_router(stock_router, tags=['stock'])

@main_router.get('/')
async def healthy_check():
    return {'Hello':'Mr. Anderson'}

app.include_router(main_router)

# origins = ["http://localhost:5173", "http://nginx"]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)