from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛒 Каталог")],
        [KeyboardButton(text="🛍 Посмотреть корзину"), KeyboardButton(text="❌ Очистить корзину")],
        [KeyboardButton(text="✅ Оформить заказ")]
    ],
    resize_keyboard=True
)

catalog_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🍔 Бургер")],
        [KeyboardButton(text="🥤 Напиток")],
        [KeyboardButton(text="назад в меню")]
    ],
    resize_keyboard=True
)

quantity_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=str(i))] for i in range(1, 6)],
    resize_keyboard=True
)

confirm_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛍 Посмотреть корзину")],
        [KeyboardButton(text="✅ Оформить заказ"), KeyboardButton(text="❌ Очистить корзину")]
    ],
    resize_keyboard=True
)

location_phone_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📍 Отправить локацию", request_location=True)],
        [KeyboardButton(text="📞 Отправить номер", request_contact=True)],
    ],
    resize_keyboard=True
)
