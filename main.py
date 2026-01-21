from fastapi import FastAPI, Request
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.constants import ParseMode
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

        # Команда /start
        if text == "/start":
            keyboard = [
                [InlineKeyboardButton("🛏 Посмотреть номера", url="https://polyana-hotel.ru/hotel-rooms/"), InlineKeyboardButton("📅 Забронировать номер", url="https://polyana-hotel.ru/bronirovanie/")],
                [InlineKeyboardButton("🗺 Как добраться", callback_data="map")],
                [InlineKeyboardButton("📞 Контакты", callback_data="contact")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await bot.send_photo(
                chat_id=chat_id,
                photo="https://polyana-hotel.ru/wp-content/uploads/2024/07/dsc05048-scaled.jpg",
                caption='Добро пожаловать в Парк-отель "Поляна"! 🏔\n\n'
                        'Я — ваш виртуальный ассистент. Работаю 24/7 и отвечу на любые вопросы об отеле:\n'
                        '🏠 Номера и коттеджи\n'
                        '💰 Цены и акции\n'
                        '🛁 Услуги (баня, бассейн, массаж)\n'
                        '🎉 Развлечения и мероприятия\n'
                        '📋 Правила и условия\n\n'
                        'Просто напишите свой вопрос, и я помогу!',
                reply_markup=reply_markup
            )
            return {"ok": True}
        
        # Команда /help
        elif text == "/help":
            keyboard = [
                [InlineKeyboardButton("🛏 Посмотреть номера", url="https://polyana-hotel.ru/hotel-rooms/"), InlineKeyboardButton("📅 Забронировать номер", url="https://polyana-hotel.ru/bronirovanie/")],
                [InlineKeyboardButton("🗺 Как добраться", callback_data="map")],
                [InlineKeyboardButton("📞 Контакты", callback_data="contact")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await bot.send_photo(
                chat_id=chat_id,
                photo="https://polyana-hotel.ru/wp-content/uploads/2023/02/territorija-49.jpg",
                caption='Я помогу с информацией об отеле "Поляна":\n'
                        '- Номера и цены\n'
                        '- Услуги (баня, бассейн, массаж)\n'
                        '- Инфраструктура и развлечения\n'
                        '- Правила проживания\n\n'
                        'Просто напишите свой вопрос или используйте кнопки ниже.',
                reply_markup=reply_markup
            )
            return {"ok": True}
        
        # Текстовые запросы → отправляем в n8n
        else:
            # Показываем "печатает..."
            await bot.send_chat_action(chat_id=chat_id, action="typing")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    N8N_WEBHOOK_URL,
                    json={"chat_id": chat_id, "user_message": text}
                )
                answer = response.json().get("text", "Произошла ошибка.")
                
                # Кнопка "Главное меню"
                keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data="basic_menu")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                # Отправляем ответ с фото и кнопкой
                await bot.send_photo(
                    chat_id=chat_id,
                    photo="https://polyana-hotel.ru/wp-content/uploads/2024/07/dsc05084-scaled.jpg",
                    caption=answer,
                    reply_markup=reply_markup
                )
            return {"ok": True}
    
    # Обработка inline-кнопок
    elif "callback_query" in data:
        callback = data["callback_query"]
        chat_id = callback["message"]["chat"]["id"]
        message_id = callback["message"]["message_id"]  # ← Добавили message_id
        callback_data = callback["data"]
        
        # Кнопка "Контакты"
        if callback_data == "contact":
            keyboard = [
                [InlineKeyboardButton("🗺 Как добраться", callback_data="map")],
                [InlineKeyboardButton("🏠 Главное меню", callback_data="basic_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await bot.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media="https://polyana-hotel.ru/wp-content/uploads/2024/07/dsc05045-scaled.jpg",
                    caption='📞 Контакты Парк-отеля "Поляна"\n\n'
                            'Телефон: `+7(988) 311-11-99`\n'
                            'Email: `recreation-area-glade@yandex.ru`\n\n'
                            '🕐 Администрация работает:\n'
                            'Ежедневно с 9:00 до 21:00\n\n'
                            'Адрес: `г. Геленджик, п. Дивноморское, ул. Короленко, 1/1`',
                    parse_mode=ParseMode.MARKDOWN
                ),
                reply_markup=reply_markup
            )
        
        # Кнопка "Как добраться"
        elif callback_data == "map":
            keyboard = [
                [InlineKeyboardButton("🚌 Общественный транспорт", url="https://yandex.kz/maps/ru/?ll=38.110555%2C44.538275&mode=routes&rtext=44.572021%2C38.090500~44.506698%2C38.136470&rtt=mt&ruri=ymapsbm1%3A%2F%2Forg%3Foid%3D1054482933~ymapsbm1%3A%2F%2Forg%3Foid%3D171223132081&z=13.62"), InlineKeyboardButton("🚗 Автомобиль", url="https://yandex.kz/maps/ru/?ll=38.114689%2C44.538643&mode=routes&rtext=44.572021%2C38.090500~44.506698%2C38.136470&rtt=auto&ruri=ymapsbm1%3A%2F%2Forg%3Foid%3D1054482933~ymapsbm1%3A%2F%2Forg%3Foid%3D171223132081&z=13.52")],
                [InlineKeyboardButton("📍 На карте", url="https://yandex.kz/maps/org/polyana/171223132081/?from=mapframe&ll=38.136466%2C44.508011&source=mapframe&utm_source=mapframe&z=17"), InlineKeyboardButton("📞 Контакты", callback_data="contact")],
                [InlineKeyboardButton("🏠 Главное меню", callback_data="basic_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await bot.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media="https://polyana-hotel.ru/wp-content/uploads/2024/07/dsc05045-scaled.jpg",
                    caption='Адрес отеля "Поляна":\n'
                            '`г. Геленджик, п. Дивноморское, ул. Короленко, 1/1`\n\n'
                            'Или выбери:\n'
                            '🚗 На автомобиле\n'
                            '🚌 Общественным транспортом\n'
                            '📍 Показать на карте',
                    parse_mode=ParseMode.MARKDOWN
                ),
                reply_markup=reply_markup
            )
        
        # Кнопка "Главное меню"
        elif callback_data == "basic_menu":
            keyboard = [
                [InlineKeyboardButton("🛏 Посмотреть номера", url="https://polyana-hotel.ru/hotel-rooms/"), InlineKeyboardButton("📅 Забронировать номер", url="https://polyana-hotel.ru/bronirovanie/")],
                [InlineKeyboardButton("🗺 Как добраться", callback_data="map")],
                [InlineKeyboardButton("📞 Контакты", callback_data="contact")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await bot.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media="https://polyana-hotel.ru/wp-content/uploads/2023/02/territorija-39.jpg",
                    caption='Готов помочь! 🏔\n'
                            'Расскажу о номерах, услугах, инфраструктуре и ценах. Что вас интересует?'
                ),
                reply_markup=reply_markup
            )
        
        await bot.answer_callback_query(callback["id"])
        return {"ok": True}
    
    return {"ok": True}

@app.get("/")
async def root():
    return {"status": "Bot is running"}
