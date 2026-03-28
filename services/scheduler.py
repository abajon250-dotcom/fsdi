from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from database import (
    get_chat_broadcast, get_active_broadcast, delete_expired_subscriptions,
    get_pending_payment, update_payment_status, log_action
)
from services.subscription import revoke_subscription, activate_subscription
from services.payment_providers import get_cryptobot_invoice_status
from config import ALLOWED_CHAT_ID

scheduler = AsyncIOScheduler()

async def broadcast_job():
    """Отправляет текст рассылки в чат, если есть активная рассылка."""
    from main import bot
    admin_text, user_text, _ = await get_chat_broadcast(ALLOWED_CHAT_ID)
    text_to_send = None
    if admin_text:
        text_to_send = admin_text
    else:
        active_broadcast = await get_active_broadcast(ALLOWED_CHAT_ID)
        if active_broadcast and user_text:
            text_to_send = user_text
    if text_to_send:
        try:
            # ОТПРАВЛЯЕМ С HTML ПАРСИНГОМ
            await bot.send_message(ALLOWED_CHAT_ID, text_to_send, parse_mode="HTML")
        except Exception as e:
            print(f"Ошибка рассылки в чат {ALLOWED_CHAT_ID}: {e}")

async def check_expired_subscriptions():
    expired = await delete_expired_subscriptions()
    for sub_id, user_id, chat_id, sub_type, data in expired:
        await revoke_subscription(user_id, chat_id, sub_type, data)

async def check_pending_payments():
    from main import bot
    from database import DB_PATH
    import aiosqlite

    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT id, user_id, chat_id, type, data, amount, currency, provider, payment_id "
            "FROM pending_payments WHERE status = 'pending' AND provider = 'cryptobot'"
        ) as cursor:
            pendings = await cursor.fetchall()

    for (pending_id, user_id, chat_id, sub_type, data, amount, currency, provider, payment_id) in pendings:
        status = await get_cryptobot_invoice_status(payment_id)
        if status == "paid":
            await update_payment_status(payment_id, provider, "paid")
            await activate_subscription(user_id, chat_id, sub_type, data)
            await log_action(user_id, "payment_confirmed", f"{sub_type} через {provider}")
            try:
                await bot.send_message(user_id, f"Ваша подписка {sub_type} активирована! Спасибо за оплату.")
            except:
                pass
        elif status in ("expired", "cancelled"):
            await update_payment_status(payment_id, provider, "failed")

def setup_scheduler():
    scheduler.add_job(broadcast_job, IntervalTrigger(minutes=30))
    scheduler.add_job(check_expired_subscriptions, IntervalTrigger(minutes=5))
    scheduler.add_job(check_pending_payments, IntervalTrigger(seconds=60))
    scheduler.start()