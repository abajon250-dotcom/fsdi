from datetime import datetime, timedelta
from database import add_subscription, set_chat_broadcast, clear_chat_broadcast

def parse_duration(duration_key: str) -> int:
    """Возвращает количество дней для заданного ключа длительности."""
    mapping = {
        "1_week": 7,
        "2_weeks": 14,
        "1_month": 30,
        "3_months": 90,
        "6_months": 180
    }
    return mapping.get(duration_key, 7)

async def activate_subscription(user_id: int, chat_id: int, sub_type: str, data: str, duration_key: str):
    """Активирует подписку на указанный срок."""
    days = parse_duration(duration_key)
    expires_at = datetime.now() + timedelta(days=days)
    await add_subscription(user_id, chat_id, sub_type, data, expires_at)

    if sub_type == "admin":
        from main import bot
        try:
            # Назначаем администратором без права назначать других админов
            await bot.promote_chat_member(
                chat_id, user_id,
                can_change_info=False,
                can_delete_messages=True,
                can_invite_users=True,
                can_restrict_members=False,
                can_pin_messages=False,
                can_promote_members=False
            )
        except Exception as e:
            print(f"Ошибка назначения админа: {e}")
    elif sub_type == "broadcast":
        await set_chat_broadcast(chat_id, data, user_id)
    elif sub_type == "prefix":
        pass

async def revoke_subscription(user_id: int, chat_id: int, sub_type: str, data: str):
    if sub_type == "admin":
        from main import bot
        try:
            # Снимаем права администратора
            await bot.promote_chat_member(
                chat_id, user_id,
                can_change_info=False,
                can_delete_messages=False,
                can_invite_users=False,
                can_restrict_members=False,
                can_pin_messages=False,
                can_promote_members=False
            )
        except Exception as e:
            print(f"Ошибка снятия админки: {e}")
    elif sub_type == "broadcast":
        from database import get_chat_broadcast, clear_chat_broadcast
        _, current_text, current_user = await get_chat_broadcast(chat_id)
        if current_user == user_id:
            await clear_chat_broadcast(chat_id)
    elif sub_type == "prefix":
        pass