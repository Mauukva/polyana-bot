# Обработка inline-кнопок
elif "callback_query" in data:
    callback = data["callback_query"]
    chat_id = callback["message"]["chat"]["id"]
    message_id = callback["message"]["message_id"]  # ← ID сообщения для редактирования
    callback_data = callback["data"]
    
    # Кнопка "Контакты"
    if callback_data == "contact":
        keyboard = [
            [InlineKeyboardButton("🗺 Как добраться", callback_data="map")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="basic_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Редактируем фото
        await bot.edit_message_media(
            chat_id=chat_id,
            message_id=message_id,
            media=InputMediaPhoto(
                media="https://polyana-hotel.ru/wp-content/uploads/2024/07/dsc05045-scaled.jpg",
                caption='📞 Контакты Парк-отеля "Поляна"\n\n'
                        'Телефон: `+7(988) 311-11-99`\n'
                        'Email: `recreation-area-polyana@yandex.ru`\n\n'
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
            [InlineKeyboardButton("🚌 Общественный транспорт", url="https://yandex.kz/maps/..."), 
             InlineKeyboardButton("🚗 Автомобиль", url="https://yandex.kz/maps/...")],
            [InlineKeyboardButton("📍 На карте", url="https://yandex.kz/maps/..."), 
             InlineKeyboardButton("📞 Контакты", callback_data="contact")],
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
            [InlineKeyboardButton("🛏 Посмотреть номера", url="https://polyana-hotel.ru/hotel-rooms/"), 
             InlineKeyboardButton("📅 Забронировать номер", url="https://polyana-hotel.ru/bronirovanie/")],
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
