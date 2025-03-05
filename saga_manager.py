import logging
import asyncio
from db import SessionLocal
from models import Order
from payment_service import process_payment, compensate_payment
from inventory_service import reserve_item, release_item
from shipping_service import ship_order, cancel_shipment

# Настраиваем логирование
logging.basicConfig(level=logging.INFO, filename="saga.log", format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def update_order_status(order_id, status):
    async with SessionLocal() as session:
        order = await session.get(Order, order_id)
        if order:
            order.status = status
            await session.commit()
            logger.info(f"🔄 Обновлен статус заказа {order_id} → {status}")

async def process_order(order_id, item_id, quantity, amount):
    """Основная Saga-цепочка"""
    logger.info(f"🚀 Начинаем обработку заказа {order_id}...")
    await update_order_status(order_id, "processing")

    # 1. Резервируем товар
    if not await reserve_item(order_id, item_id, quantity):  
        logger.error(f"❌ Отмена заказа {order_id} (не хватает товара)")
        await update_order_status(order_id, "failed")
        return False

    # 2. Обрабатываем оплату
    if not await process_payment(order_id, amount):  
        logger.error(f"❌ Отмена заказа {order_id} (оплата не прошла)")
        await release_item(order_id, item_id, quantity)  
        await update_order_status(order_id, "failed")
        return False

    # 3. Отправляем заказ
    if not await ship_order(order_id):  
        logger.error(f"❌ Отмена заказа {order_id} (ошибка при отправке)")
        await compensate_payment(order_id)  
        await release_item(order_id, item_id, quantity)  
        await update_order_status(order_id, "failed")
        return False

    logger.info(f"✅ Заказ {order_id} успешно выполнен!")
    await update_order_status(order_id, "completed")
    return True
