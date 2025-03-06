from .decorators import *

from fastapi import APIRouter, HTTPException
from sqlalchemy import delete
from database import Agents, async_session
from handlers import get_all_agents_data


agents_router = APIRouter(prefix='/agents')

@agents_router.post('/create')
async def create_all_agents():
    try:
        async with async_session() as db:
            data = get_all_agents_data()
            
            for item in data:
                assortment = Agents(**item)
                db.add(assortment)

            await db.commit()
            return {"message": "Data added successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@agents_router.delete('/delete')
async def delete_all_agents():
    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(Agents))
            await session.commit()
    return {"message": "All rows were deleted"}

@agents_router.put('/update')
async def update_agents():
    pass

@agents_router.get('/get')
async def get_agents():
    pass