# keyboards.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

def main_menu():
    keyboard = [
        [InlineKeyboardButton("📋 Все запросы", callback_data="all_requests")],
        [InlineKeyboardButton("➕ Создать запрос", callback_data="create_request")],
        [InlineKeyboardButton("📌 Мои запросы", callback_data="my_requests")],
        [InlineKeyboardButton("🚗 Коммерческая помощь", callback_data="commercial")],
        [InlineKeyboardButton("🏙️ Сменить город", callback_data="change_city")]
    ]
    return InlineKeyboardMarkup(keyboard)

def categories_menu():
    keyboard = [
        [InlineKeyboardButton("🔧 Поломка", callback_data="category_breakdown")],
        [InlineKeyboardButton("⛽ Кончился бензин", callback_data="category_no_gas")],
        [InlineKeyboardButton("🚜 Застрял", callback_data="category_stuck")],
        [InlineKeyboardButton("🛠️ Другое", callback_data="category_other")]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад", callback_data="main_menu")]])

def cities_list():
    # Можно заменить на динамический список
    cities = ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург"]
    keyboard = [[InlineKeyboardButton(city, callback_data=f"set_city_{city}")] for city in cities]
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)
