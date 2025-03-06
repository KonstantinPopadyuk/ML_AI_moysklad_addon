from fastapi import APIRouter, HTTPException

from sqlalchemy import delete
from database import Assortment, async_session
from handlers import get_assorment_data


assortment_router = APIRouter(prefix='/assortment')

@assortment_router.post('/create')
async def create_all_assortment():
    try:
        async with async_session() as db:
            data = get_assorment_data()

            for item in data:
                assortment = Assortment(**item)
                db.add(assortment)

            await db.commit()
            return {"message": "Data added successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@assortment_router.delete('/delete')
async def delete_all_assortment():
    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(Assortment))
            await session.commit()
    return {"message": "All rows were deleted"}

@assortment_router.put('/update')
async def update_assortment():
    pass

@assortment_router.get('/get')
async def get_assortment():
    pass