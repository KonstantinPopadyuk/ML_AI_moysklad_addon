from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from settings import settings
import pandas as pd
from sqlalchemy.sql import text
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
    logger.info(f'start to sync read {settings.SQLALCHEMY_SYNC_DB_URL}')
    engine = create_engine(settings.SQLALCHEMY_SYNC_DB_URL)
    logger.info(f'start to sync read {engine=}')
    # df = pd.read_sql(query, engine)
    with engine.connect() as conn:
        df = pd.read_sql(
            sql=query,
            con=conn.connection
        )

    logger.info(f'df {df=}')
    if df.empty:
        logger.error("Suprisingly no data was retrieved from the database. DataFrame is empty.")
        logger.error(f"Current query was {engine=}")
    return df