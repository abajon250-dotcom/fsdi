import aiohttp
from config import CRYPTOBOT_TOKEN, CRYPTOBOT_API_URL, XROCKET_API_KEY

async def create_cryptobot_invoice(amount: float, description: str):
    url = f"{CRYPTOBOT_API_URL}/createInvoice"
    headers = {"Crypto-Pay-API-Token": CRYPTOBOT_TOKEN}
    data = {
        "asset": "USDT",
        "amount": amount,
        "description": description,
        "paid_btn_name": "callback",
        "paid_btn_url": "https://t.me/your_bot?start=payment_done"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as resp:
            if resp.status == 200:
                result = await resp.json()
                if result.get("ok"):
                    return result["result"]
    return None

async def create_xrocket_invoice(amount: float, description: str):
    # Здесь должна быть реальная интеграция с Xrocket
    return None

async def get_cryptobot_invoice_status(invoice_id: str):
    url = f"{CRYPTOBOT_API_URL}/getInvoices"
    headers = {"Crypto-Pay-API-Token": CRYPTOBOT_TOKEN}
    params = {"invoice_ids": invoice_id}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as resp:
            if resp.status == 200:
                result = await resp.json()
                if result.get("ok") and result["result"]["items"]:
                    return result["result"]["items"][0]["status"]
import aiohttp
from config import CRYPTOBOT_TOKEN, CRYPTOBOT_API_URL, XROCKET_API_KEY

async def create_cryptobot_invoice(amount: float, description: str):
    url = f"{CRYPTOBOT_API_URL}/createInvoice"
    headers = {"Crypto-Pay-API-Token": CRYPTOBOT_TOKEN}
    data = {
        "asset": "USDT",
        "amount": amount,
        "description": description,
        "paid_btn_name": "callback",
        "paid_btn_url": "https://t.me/your_bot?start=payment_done"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as resp:
            if resp.status == 200:
                result = await resp.json()
                if result.get("ok"):
                    return result["result"]
    return None

async def create_xrocket_invoice(amount: float, description: str):
    # Замените на реальную интеграцию
    # url = "https://api.xrocket.com/v1/invoice"
    # headers = {"Authorization": f"Bearer {XROCKET_API_KEY}"}
    # payload = {"amount": amount, "currency": "USD", "description": description}
    # async with aiohttp.ClientSession() as session:
    #     async with session.post(url, headers=headers, json=payload) as resp:
    #         if resp.status == 200:
    #             data = await resp.json()
    #             return {"id": data["invoice_id"], "pay_url": data["payment_link"]}
    return None

async def get_cryptobot_invoice_status(invoice_id: str):
    url = f"{CRYPTOBOT_API_URL}/getInvoices"
    headers = {"Crypto-Pay-API-Token": CRYPTOBOT_TOKEN}
    params = {"invoice_ids": invoice_id}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as resp:
            if resp.status == 200:
                result = await resp.json()
                if result.get("ok") and result["result"]["items"]:
                    return result["result"]["items"][0]["status"]
    return None