from sqlalchemy.ext.asyncio import AsyncSession
from db import SessionLocal
from models import Shipping

async def ship_order(order_id):
    async with SessionLocal() as session:
        try:
            shipping = Shipping(order_id=order_id, shipped=True)
            session.add(shipping)
            await session.commit()
            print(f"✅ Заказ {order_id} отправлен!")
            return True
        except Exception as e:
            await session.rollback()
            print(f"❌ Ошибка при отправке заказа {order_id}: {e}")
            return False

async def cancel_shipment(order_id):
    async with SessionLocal() as session:
        try:
            shipping = await session.get(Shipping, order_id)
            if shipping:
                await session.delete(shipping)
                await session.commit()
                print(f"🔄 Отправка отменена для заказа {order_id}")
        except Exception as e:
            await session.rollback()
            print(f"❌ Ошибка при отмене отправки: {e}")
