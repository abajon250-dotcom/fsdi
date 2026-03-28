from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database import add_user, log_action, is_admin
from services.payment_providers import create_cryptobot_invoice, create_xrocket_invoice
from config import PRICES, ALLOWED_CHAT_ID, CUSTOM_EMOJI_IDS, CUSTOM_EMOJIS

router = Router()

class BuySubscription(StatesGroup):
    entering_text = State()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await add_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
    await log_action(message.from_user.id, "start", "запустил бота")
    await state.clear()

    # Кнопки с кастомными эмодзи (icon_custom_emoji_id)
    admin_btn = InlineKeyboardButton(
        text="Купить админку",
        callback_data="buy_admin",
        icon_custom_emoji_id=CUSTOM_EMOJI_IDS["admin"]
    )
    broadcast_btn = InlineKeyboardButton(
        text="Купить рассылку",
        callback_data="buy_broadcast",
        icon_custom_emoji_id=CUSTOM_EMOJI_IDS["broadcast"]
    )
    prefix_btn = InlineKeyboardButton(
        text="Купить префикс",
        callback_data="buy_prefix",
        icon_custom_emoji_id=CUSTOM_EMOJI_IDS["stats"]
    )
    my_subs_btn = InlineKeyboardButton(
        text="Мои подписки",
        callback_data="my_subs",
        icon_custom_emoji_id=CUSTOM_EMOJI_IDS["my_subs"]
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [admin_btn],
        [broadcast_btn],
        [prefix_btn],
        [my_subs_btn]
    ])
    if await is_admin(message.from_user.id):
        admin_panel_btn = InlineKeyboardButton(
            text="Админ-панель",
            callback_data="admin_panel",
            icon_custom_emoji_id=CUSTOM_EMOJI_IDS["admin_panel"]
        )
        keyboard.inline_keyboard.append([admin_panel_btn])

    await message.answer(
        f"{CUSTOM_EMOJIS['greeting']} Добро пожаловать! Выберите действие:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@router.callback_query(F.data == "buy_admin")
async def buy_admin(callback: CallbackQuery, state: FSMContext):
    await state.update_data(sub_type="admin", data_text="")
    await show_payment_options(callback.message, "admin", "", state)
    await callback.answer()

@router.callback_query(F.data == "buy_broadcast")
async def buy_broadcast(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите текст для рассылки (будет отправляться каждые 30 минут):")
    await state.set_state(BuySubscription.entering_text)
    await state.update_data(sub_type="broadcast")
    await callback.answer()

@router.callback_query(F.data == "buy_prefix")
async def buy_prefix(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите текст префикса (например, [VIP]):")
    await state.set_state(BuySubscription.entering_text)
    await state.update_data(sub_type="prefix")
    await callback.answer()

@router.message(BuySubscription.entering_text)
async def process_text(message: Message, state: FSMContext):
    text = message.text.strip()
    if not text:
        await message.answer("Текст не может быть пустым.")
        return
    data = await state.get_data()
    sub_type = data["sub_type"]
    await state.update_data(data_text=text)
    await show_payment_options(message, sub_type, text, state)

async def show_payment_options(message: Message, sub_type: str, data_text: str, state: FSMContext):
    amount = PRICES[f"{sub_type}_week"]
    cryptobot_btn = InlineKeyboardButton(
        text="CryptoBot",
        callback_data=f"pay_cryptobot_{sub_type}_{data_text}",
        icon_custom_emoji_id=CUSTOM_EMOJI_IDS["stats"]
    )
    xrocket_btn = InlineKeyboardButton(
        text="Xrocket",
        callback_data=f"pay_xrocket_{sub_type}_{data_text}",
        icon_custom_emoji_id=CUSTOM_EMOJI_IDS["broadcast"]
    )
    back_btn = InlineKeyboardButton(
        text="Назад",
        callback_data="back_to_start",
        icon_custom_emoji_id=CUSTOM_EMOJI_IDS["back"]
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [cryptobot_btn],
        [xrocket_btn],
        [back_btn]
    ])
    await message.answer(f"Выберите способ оплаты. Стоимость: {amount} USD.", reply_markup=keyboard)

@router.callback_query(F.data.startswith("pay_"))
async def process_payment(callback: CallbackQuery, state: FSMContext):
    data_parts = callback.data.split("_")
    provider = data_parts[1]
    sub_type = data_parts[2]
    data_text = data_parts[3] if len(data_parts) > 3 else ""
    user_id = callback.from_user.id

    amount = PRICES[f"{sub_type}_week"]
    currency = "USD"

    if provider == "cryptobot":
        invoice = await create_cryptobot_invoice(amount, f"Подписка {sub_type} на неделю")
        if invoice:
            from database import add_pending_payment
            payment_id = invoice["invoice_id"]
            await add_pending_payment(user_id, ALLOWED_CHAT_ID, sub_type, data_text, amount, currency, provider, payment_id)
            await callback.message.answer(f"Оплатите по ссылке: {invoice['pay_url']}\nПосле оплаты подписка активируется автоматически.")
        else:
            await callback.message.answer("Ошибка создания счёта CryptoBot.")
    elif provider == "xrocket":
        invoice = await create_xrocket_invoice(amount, f"Подписка {sub_type} на неделю")
        if invoice:
            from database import add_pending_payment
            payment_id = invoice["id"]
            await add_pending_payment(user_id, ALLOWED_CHAT_ID, sub_type, data_text, amount, currency, provider, payment_id)
            await callback.message.answer(f"Оплатите по ссылке: {invoice['pay_url']}\nПосле оплаты подписка активируется автоматически.")
        else:
            await callback.message.answer("Ошибка создания счёта Xrocket.")
    await callback.answer()

@router.callback_query(F.data == "back_to_start")
async def back_to_start(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await cmd_start(callback.message, state)
    await callback.answer()

@router.callback_query(F.data == "my_subs")
async def my_subscriptions(callback: CallbackQuery):
    await callback.message.answer("Информация о подписках пока не реализована.")
    await callback.answer()

@router.callback_query(F.data == "admin_panel")
async def go_to_admin_panel(callback: CallbackQuery):
    if not await is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return
    from handlers.admin_panel import admin_panel
    await admin_panel(callback.message)
    await callback.answer()