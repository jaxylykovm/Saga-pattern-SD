from sqlalchemy.ext.asyncio import AsyncSession
from db import SessionLocal
from models import Payment

async def process_payment(order_id, amount):
    async with SessionLocal() as session:
        try:
            payment = Payment(order_id=order_id, status="PAID")
            session.add(payment)
            await session.commit()
            print(f"✅ Оплата успешно проведена для заказа {order_id}")
            return True
        except Exception as e:
            await session.rollback()
            print(f"❌ Ошибка при оплате заказа {order_id}: {e}")
            return False

async def compensate_payment(order_id):
    async with SessionLocal() as session:
        try:
            payment = await session.get(Payment, order_id)
            if payment:
                await session.delete(payment)
                await session.commit()
                print(f"🔄 Оплата отменена для заказа {order_id}")
        except Exception as e:
            await session.rollback()
            print(f"❌ Ошибка при отмене оплаты: {e}")
