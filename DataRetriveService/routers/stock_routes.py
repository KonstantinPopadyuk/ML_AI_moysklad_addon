from fastapi import APIRouter, HTTPException
from sqlalchemy import delete
from database import Stock, async_session
from handlers import get_stock_data


stock_router = APIRouter(prefix='/stock')

@stock_router.post('/create')
async def create_all_stock():
    try:
        db = async_session()
        data = get_stock_data()

        for item in data:
            stock = Stock(**item)
            db.add(stock)

        await db.commit()
        return {"message":"Stock data was added successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await db.close()

@stock_router.delete('/delete')
async def delete_all_stock():
    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(Stock))
            await session.commit()
    return {"message": "All rows were deleted"}

@stock_router.put('/update')
async def update_stock():
    pass

@stock_router.get('/get')
async def get_stock():
    pass