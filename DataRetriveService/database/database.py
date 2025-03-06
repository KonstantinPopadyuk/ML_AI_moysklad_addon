from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from settings import settings
import pandas as pd
from sqlalchemy.sql import text


engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL, future=True, echo=False)
async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def get_db():
    try:
        session = await async_session()
        yield session
    finally:
        await session.close()


async def async_read_data(query: str):
    """
    Читает данные из базы данных с помощью заданного запроса.

    Args:
        query: SQL запрос для выборки данных.

    Returns:
        pandas.DataFrame: DataFrame с данными.
    """
    async with async_session() as session:
        result = await session.execute(text(query))
        data = result.all()
        df = pd.DataFrame(data)
        return df
    

def read_data_sync(query: str) -> pd.DataFrame:
    engine = create_engine(settings.SQLALCHEMY_SYNC_DB_URL)
    df = pd.read_sql(query, engine)
    return df