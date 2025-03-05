from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "postgresql+asyncpg://magzhanjaxylykov@localhost:5432/saga_checkout"

engine = create_async_engine(DATABASE_URL, echo=True)
