import os
import json
from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart

from config import ADMIN_ID
from keyboards import (
    main_menu, catalog_menu, confirm_menu,
    location_phone_menu, quantity_menu
)

router = Router()

user_data = {}
cart_data = {}

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}!\n👋 Добро пожаловать в бот доставки!",
        reply_markup=main_menu
    )

@router.message(F.text == "🛒 Каталог")
async def show_catalog(message: Message):
    await message.answer("Выберите товар:", reply_markup=catalog_menu)

@router.message(F.text.in_(["🍔 Бургер", "🥤 Напиток"]))
async def select_product(message: Message):
    user_id = message.from_user.id
    product = message.text
    prices = {"🍔 Бургер": 20000, "🥤 Напиток": 10000}
    user_data[user_id] = {"product": product, "price": prices[product]}
    await message.answer(f"Сколько '{product}' вы хотите заказать?", reply_markup=quantity_menu)

@router.message(F.text.in_([str(i) for i in range(1, 6)]))
async def set_quantity(message: Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        return await message.answer("Сначала выберите товар.")

    quantity = int(message.text)
    item = user_data.pop(user_id)
    cart = cart_data.setdefault(user_id, {})
    name = item["product"]

    if name in cart:
        cart[name]["quantity"] += quantity
    else:
        cart[name] = {"price": item["price"], "quantity": quantity}

    await message.answer(f"✅ Добавлено в корзину: {name} — {quantity} шт.", reply_markup=confirm_menu)

@router.message(F.text == "🛍 Посмотреть корзину")
async def show_cart(message: Message):
    user_id = message.from_user.id
    cart = cart_data.get(user_id)
    if not cart:
        return await message.answer("Ваша корзина пуста.")
    
    text = "<b>🛒 Ваша корзина:</b>\n\n"
    total = 0
    for name, item in cart.items():
        subtotal = item["price"] * item["quantity"]
        total += subtotal
        text += f"{name} — {item['quantity']} x {item['price']} = {subtotal} сум\n"
    text += f"\n<b>Итого:</b> {total} сум"

    await message.answer(text, reply_markup=confirm_menu)

@router.message(F.text == "❌ Очистить корзину")
async def clear_cart(message: Message):
    user_id = message.from_user.id
    cart_data.pop(user_id, None)
    await message.answer("🗑 Корзина очищена.", reply_markup=main_menu)

@router.message(F.text == "✅ Оформить заказ")
async def checkout_order(message: Message):
    user_id = message.from_user.id
    cart = cart_data.get(user_id)
    if not cart:
        return await message.answer("Ваша корзина пуста.")
    
    total = sum(item["price"] * item["quantity"] for item in cart.values())

    text = "<b>🧾 Ваш заказ:</b>\n\n"
    for name, item in cart.items():
        text += f"{name} — {item['quantity']} x {item['price']} = {item['quantity'] * item['price']} сум\n"
    text += f"\n<b>Итого:</b> {total} сум"

    await message.answer(text, reply_markup=location_phone_menu)

@router.message(F.location)
async def get_location(message: Message):
    user_id = message.from_user.id
    if user_id not in cart_data:
        return await message.answer("Сначала оформите заказ.")

    cart_data[user_id]["latitude"] = message.location.latitude
    cart_data[user_id]["longitude"] = message.location.longitude
    await message.answer("📞 Теперь отправьте свой номер", reply_markup=location_phone_menu)

@router.message(F.contact)
async def get_contact(message: Message):
    user_id = message.from_user.id
    if user_id not in cart_data:
        return await message.answer("Сначала оформите заказ.")

    cart_data[user_id]["phone"] = message.contact.phone_number

    # Сохраняем заказ
    if not os.path.exists("orders.json"):
        with open("orders.json", "w") as f:
            json.dump([], f)

    with open("orders.json", "r") as f:
        orders = json.load(f)

    order = cart_data[user_id]
    orders.append(order)

    with open("orders.json", "w") as f:
        json.dump(orders, f, indent=4)

    # Уведомляем админа
    text = "<b>📦 Новый заказ:</b>\n\n"
    for name, item in order.items():
        if isinstance(item, dict):
            text += f"{name} — {item['quantity']} x {item['price']} = {item['quantity'] * item['price']} сум\n"
    text += (
        f"\nТелефон: {order['phone']}\n"
        f"🌍 https://maps.google.com/?q={order['latitude']},{order['longitude']}"
    )

    await message.bot.send_message(ADMIN_ID, text)
    await message.answer("✅ Ваш заказ отправлен!", reply_markup=ReplyKeyboardRemove())
    await message.answer("📦 Возвращаемся в главное меню", reply_markup=main_menu)
    cart_data.pop(user_id)
