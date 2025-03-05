from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# Создаем асинхронный движок для PostgreSQL
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаем фабрику асинхронных сессий
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Функция для получения сессии
async def get_db():
    async with SessionLocal() as session:
        yield session
