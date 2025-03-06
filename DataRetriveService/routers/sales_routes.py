from fastapi import APIRouter, HTTPException
from sqlalchemy import delete
from database import Sales, async_session
from handlers import get_sales_data


sales_router = APIRouter(prefix='/sales')

@sales_router.post('/create')
async def create_all_sales():
    try:
        db = async_session()
        data = get_sales_data()

        for item in data:
            sales = Sales(**item)
            db.add(sales)

        await db.commit()
        return {"message":"Sales data was added successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await db.close()

@sales_router.delete('/delete')
async def delete_all_sales():
    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(Sales))
            await session.commit()
    return {"message": "All rows were deleted"}

@sales_router.put('/update')
async def update_sales():
    pass

@sales_router.get('/get')
async def get_sales():
    pass