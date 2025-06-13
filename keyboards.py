from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Главное меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛒 Каталог")],
        [KeyboardButton(text="🛍 Посмотреть корзину"), KeyboardButton(text="✅ Оформить заказ")]
    ],
    resize_keyboard=True
)

# Каталог товаров
catalog_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🍕 Пицца"), KeyboardButton(text="🍔 Бургер")],
        [KeyboardButton(text="🥤 Напиток")],
        [KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True
)

# Меню подтверждения/оформления
confirm_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Оформить заказ")],
        [KeyboardButton(text="🛍 Посмотреть корзину"), KeyboardButton(text="❌ Очистить корзину")],
        [KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True
)

# Выбор количества товара
quantity_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="1"), KeyboardButton(text="2"), KeyboardButton(text="3")],
        [KeyboardButton(text="4"), KeyboardButton(text="5")]
    ],
    resize_keyboard=True
)

# Кнопки отправки локации и номера
location_phone_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📍 Отправить локацию", request_location=True)],
        [KeyboardButton(text="📞 Отправить номер", request_contact=True)]
    ],
    resize_keyboard=True
)

# Админ-панель
admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Все заказы")],
        [KeyboardButton(text="🗑 Удалить все заказы")],
        [KeyboardButton(text="📊 Статистика заказов")],
        [KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True
)
