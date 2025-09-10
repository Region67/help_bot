# Перезапишем bot.py с исправленным кодом
cat > /root/help_bot/bot.py << 'EOF'
# bot.py
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import config
import database
import keyboards
import messages

# Инициализация БД
database.init_db()

# Обработчики
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = database.get_user(update.effective_user.id)
    if not user or not user[1]:  # Если нет города
        await update.message.reply_text(messages.CHOOSE_CITY, reply_markup=keyboards.cities_list())
    else:
        await update.message.reply_text("Главное меню:", reply_markup=keyboards.main_menu())

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user = database.get_user(user_id)
    data = query.data

    if data.startswith("set_city_"):
        city = data.split("_", 2)[2]
        database.set_user_city(user_id, city)
        await query.edit_message_text("Город установлен!", reply_markup=keyboards.main_menu())

    elif data == "main_menu":
        await query.edit_message_text("Главное меню:", reply_markup=keyboards.main_menu())

    elif data == "all_requests":
        if not user:
            await query.edit_message_text("Сначала выберите город.", reply_markup=keyboards.cities_list())
            return
        city = user[1]
        requests = database.get_requests_by_city(city)
        if not requests:
            await query.edit_message_text(messages.NO_REQUESTS, reply_markup=keyboards.back_button())
            return
        text = "\n\n".join([f"📞 {r[5]}\n👤 @{r[6]}\n📝 {r[4]}\n📷" + (f"[Фото](tg://file/{r[7]})" if r[7] else "Нет") for r in requests])
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboards.back_button())

    elif data == "create_request":
        await query.edit_message_text("Выберите категорию:", reply_markup=keyboards.categories_menu())

    elif data.startswith("category_"):
        context.user_data['category'] = data.split("_")[1]
        await query.edit_message_text("Введите описание проблемы:")

    elif data == "my_requests":
        my_requests = database.get_user_requests(user_id)
        if not my_requests:
            await query.edit_message_text("У вас нет запросов.", reply_markup=keyboards.back_button())
            return
        buttons = [[InlineKeyboardButton(f"Запрос {r[0]}: {r[4][:20]}...", callback_data=f"view_request_{r[0]}")] for r in my_requests]
        buttons.append([InlineKeyboardButton("⬅️ Назад", callback_data="main_menu")])
        await query.edit_message_text("Ваши запросы:", reply_markup=InlineKeyboardMarkup(buttons))

    elif data.startswith("view_request_"):
        req_id = int(data.split("_")[-1])
        # Тут можно добавить редактирование/закрытие
        await query.edit_message_text(f"Запрос ID: {req_id}. Здесь будет кнопка 'Закрыть'", reply_markup=keyboards.back_button())

    elif data == "commercial":
        await query.edit_message_text("Коммерческая помощь (платные услуги). Скоро...", reply_markup=keyboards.back_button())

    elif data == "change_city":
        await query.edit_message_text(messages.CHOOSE_CITY, reply_markup=keyboards.cities_list())

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'category' in context.user_data:
        category = context.user_data['category']
        user = database.get_user(update.effective_user.id)
        if not user:
            await update.message.reply_text("Ошибка. Перезапустите бота.")
            return
        city = user[1]
        phone = update.message.contact.phone_number if update.message.contact else "Не указан"
        username = update.effective_user.username or "Нет"
        photo_id = None
        if update.message.photo:
            photo_id = update.message.photo[-1].file_id
        database.create_request(
            user_id=update.effective_user.id,
            city=city,
            category=category,
            description=update.message.text,
            phone=phone,
            username=username,
            photo_id=photo_id
        )
        del context.user_data['category']
        await update.message.reply_text(messages.REQUEST_CREATED, reply_markup=keyboards.main_menu())
    else:
        await update.message.reply_text("Пожалуйста, сначала выберите категорию через меню.", reply_markup=keyboards.main_menu())

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'category' in context.user_data:
        await update.message.reply_text("Пожалуйста, сначала введите описание проблемы.")
    else:
        await update.message.reply_text("Пожалуйста, сначала выберите категорию через меню.", reply_markup=keyboards.main_menu())

def main():
    app = Application.builder().token(config.TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()
EOF
