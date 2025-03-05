import asyncio
from saga_manager import process_order

async def run_test():
    order_id = 1
    item_id = 101
    quantity = 2
    amount = 500

    result = await process_order(order_id, item_id, quantity, amount)

    if result:
        print(f"✅ Тест заказа {order_id} прошел успешно!")
    else:
        print(f"❌ Тест заказа {order_id} провалился!")

if __name__ == "__main__":
    asyncio.run(run_test())
