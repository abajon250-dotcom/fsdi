<<<<<<< HEAD
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print(f"ОШИБКА: BOT_TOKEN не найден в {env_path}")
    exit(1)

CRYPTOBOT_TOKEN = os.getenv("CRYPTOBOT_TOKEN")
CRYPTOBOT_API_URL = "https://pay.crypt.bot/api"
XROCKET_API_KEY = os.getenv("XROCKET_API_KEY")
ALLOWED_CHAT_ID = int(os.getenv("ALLOWED_CHAT_ID", -1001234567890))
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", 0))
OWNER_ID = int(os.getenv("OWNER_ID", 0))

# Цены подписок (в долларах США)
SUBSCRIPTION_PRICES = {
    "admin": {
        "1_week": 33,
        "2_weeks": 40,
        "1_month": 60
    },
    "broadcast": {
        "1_week": 21,
        "2_weeks": 30,
        "1_month": 70
    },
    "prefix": {
        "1_month": 25,
        "3_months": 70,
        "6_months": 110
    }
}

# Длительность в днях для каждого типа и срока
DURATIONS = {
    "admin": {
        "1_week": 7,
        "2_weeks": 14,
        "1_month": 30
    },
    "broadcast": {
        "1_week": 7,
        "2_weeks": 14,
        "1_month": 30
    },
    "prefix": {
        "1_month": 30,
        "3_months": 90,
        "6_months": 180
    }
}

# ID кастомных премиум-эмодзи (вставьте свои)
CUSTOM_EMOJI_IDS = {
    "stats": "5197313098523889805",
    "broadcast": "5215346626817713558",
    "admin": "5251203410396458957",
    "logs": "5424972470023104089",
    "list": "5395695537687123235",
    "add": "5406683434124859552",
    "close": "5406683434124859552",
    "back": "5395695537687123235",
    "success": "5251203410396458957",
    "error": "5215346626817713558",
    "wait": "5424972470023104089",
    "user": "5197313098523889805",
    "subscription": "5395695537687123235",
    "greeting": "5278611606756942667",
    "my_subs": "5278578973595427038",
    "pinned": "5278528159837348960",
    "admin_panel": "5276262671962892944",
    "top_up": "5276398496008663230",
    "pin_week": "5274099962655816924",
    "prefix_month": "5447410659077661506",
    "autoposting": "5258514780469075716",
    "buy_ad": "5409048419211682843",
}

# HTML-теги для текстовых сообщений
CUSTOM_EMOJIS = {
    key: f'<tg-emoji emoji-id="{CUSTOM_EMOJI_IDS[key]}">😎</tg-emoji>' for key in CUSTOM_EMOJI_IDS
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print(f"ОШИБКА: BOT_TOKEN не найден в {env_path}")
    exit(1)

CRYPTOBOT_TOKEN = os.getenv("CRYPTOBOT_TOKEN")
CRYPTOBOT_API_URL = "https://pay.crypt.bot/api"
XROCKET_API_KEY = os.getenv("XROCKET_API_KEY")
ALLOWED_CHAT_ID = int(os.getenv("ALLOWED_CHAT_ID", -1001234567890))
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", 0))
OWNER_ID = int(os.getenv("OWNER_ID", 0))

PRICES = {
    "admin_week": 30,
    "broadcast_week": 30,
    "prefix_week": 30,
}

# ID кастомных эмодзи (премиум) для кнопок и сообщений
CUSTOM_EMOJI_IDS = {
    # старые ID (оставим для совместимости)
    "stats": "5275979556308674886",
    "broadcast": "5278528159837348960",
    "admin": "5276262671962892944",        # для кнопки "Купить админку"
    "logs": "5424972470023104089",
    "list": "5395695537687123235",
    "add": "5406683434124859552",
    "close": "5406683434124859552",
    "back": "5395695537687123235",
    "success": "5251203410396458957",
    "error": "5215346626817713558",
    "wait": "5424972470023104089",
    "user": "5197313098523889805",
    "subscription": "5395695537687123235",   # старый для "Мои подписки" – заменим новым

    # НОВЫЕ ID (данные вами)
    "greeting": "5278611606756942667",       # приветствие
    "my_subs": "5278578973595427038",        # свои подписки (заменит старый subscription)
    "pinned": "5278528159837348960",         # закреп (для админ-рассылки)
    "admin_panel": "5276262671962892944",    # админка (для кнопки админ-панели)
    "top_up": "5276398496008663230",         # пополнить баланс (если будет использоваться)
}

# HTML-теги для кастомных эмодзи в тексте (только для сообщений)
CUSTOM_EMOJIS = {
    "stats": f'<tg-emoji emoji-id="{CUSTOM_EMOJI_IDS["stats"]}">📊</tg-emoji>',
    "broadcast": f'<tg-emoji emoji-id="{CUSTOM_EMOJI_IDS["broadcast"]}">📢</tg-emoji>',
    "admin": f'<tg-emoji emoji-id="{CUSTOM_EMOJI_IDS["admin"]}">🔧</tg-emoji>',
    "logs": f'<tg-emoji emoji-id="{CUSTOM_EMOJI_IDS["logs"]}">📜</tg-emoji>',
    "back": f'<tg-emoji emoji-id="{CUSTOM_EMOJI_IDS["back"]}">◀</tg-emoji>',
    "close": f'<tg-emoji emoji-id="{CUSTOM_EMOJI_IDS["close"]}">❌</tg-emoji>',
    "success": f'<tg-emoji emoji-id="{CUSTOM_EMOJI_IDS["success"]}">✅</tg-emoji>',
    "error": f'<tg-emoji emoji-id="{CUSTOM_EMOJI_IDS["error"]}">❌</tg-emoji>',
    "wait": f'<tg-emoji emoji-id="{CUSTOM_EMOJI_IDS["wait"]}">⏳</tg-emoji>',
    "user": f'<tg-emoji emoji-id="{CUSTOM_EMOJI_IDS["user"]}">👤</tg-emoji>',
    "subscription": f'<tg-emoji emoji-id="{CUSTOM_EMOJI_IDS["my_subs"]}">💰</tg-emoji>',
    "greeting": f'<tg-emoji emoji-id="{CUSTOM_EMOJI_IDS["greeting"]}">👋</tg-emoji>',
    "pinned": f'<tg-emoji emoji-id="{CUSTOM_EMOJI_IDS["pinned"]}">📌</tg-emoji>',
    "admin_panel": f'<tg-emoji emoji-id="{CUSTOM_EMOJI_IDS["admin_panel"]}">🛡️</tg-emoji>',
    "top_up": f'<tg-emoji emoji-id="{CUSTOM_EMOJI_IDS["top_up"]}">💰</tg-emoji>',
}