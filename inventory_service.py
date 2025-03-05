from sqlalchemy.ext.asyncio import AsyncSession
from db import SessionLocal
from models import Inventory

async def reserve_item(order_id, item_id, quantity):
    async with SessionLocal() as session:
        try:
            item = await session.get(Inventory, item_id)
            if item and item.stock >= quantity:
                item.stock -= quantity
                await session.commit()
                print(f"✅ Товар {item_id} зарезервирован для заказа {order_id}")
                return True
            print(f"❌ Недостаточно товара {item_id} для заказа {order_id}")
            return False
        except Exception as e:
            await session.rollback()
            print(f"❌ Ошибка при резервировании товара: {e}")
            return False

async def release_item(order_id, item_id, quantity):
    async with SessionLocal() as session:
        try:
            item = await session.get(Inventory, item_id)
            if item:
                item.stock += quantity
                await session.commit()
                print(f"🔄 Товар {item_id} возвращен на склад после отмены заказа {order_id}")
        except Exception as e:
            await session.rollback()
            print(f"❌ Ошибка при возврате товара: {e}")
