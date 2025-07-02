import httpx

from app.core.config import settings


async def notify_telegram(text: str):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": settings.TELEGRAM_CHAT_ID, "text": text}
    async with httpx.AsyncClient() as client:
        await client.post(url, data=payload)
