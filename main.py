from fastapi import FastAPI, Request
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
import httpx
import os

app = FastAPI()
bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    
    if "message" in data:
        message = data["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "")
        
        if text == "/start":
            keyboard = [
                [InlineKeyboardButton("📞 Контакты", callback_data="contact")],
                [InlineKeyboardButton("🗺 Карта", callback_data="map")],
                [InlineKeyboardButton("📋 Меню", callback_data="menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await bot.send_message(
                chat_id=chat_id,
                text="Здравствуйте! Я помощник отеля \"Поляна\".\nЧем могу помочь?",
                reply_markup=reply_markup
            )
            return {"ok": True}
        
        else:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    N8N_WEBHOOK_URL,
                    json={"chat_id": chat_id, "user_message": text}
                )
                answer = response.json().get("text", "Произошла ошибка.")
                await bot.send_message(chat_id=chat_id, text=answer)
            return {"ok": True}
    
    elif "callback_query" in data:
        callback = data["callback_query"]
        chat_id = callback["message"]["chat"]["id"]
        callback_data = callback["data"]
        
        if callback_data == "contact":
            await bot.send_message(
                chat_id=chat_id,
                text="📞 Контакты отеля \"Поляна\"\n\nТелефон: 8 (988) 311-11-99"
            )
        elif callback_data == "map":
            await bot.send_location(
                chat_id=chat_id,
                latitude=43.5855,
                longitude=39.7231
            )
        elif callback_data == "menu":
            await bot.send_message(
                chat_id=chat_id,
                text="📋 Основное меню:\n\n1. Номера и цены\n2. Услуги\n3. Контакты"
            )
        
        await bot.answer_callback_query(callback["id"])
        return {"ok": True}
    
    return {"ok": True}

@app.get("/")
async def root():
    return {"status": "Bot is running"}
