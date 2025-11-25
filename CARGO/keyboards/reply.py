from telebot import types

# Головне меню
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🚚 Розрахувати доставку")
    btn2 = types.KeyboardButton("👤 Мій кабінет")
    btn3 = types.KeyboardButton("ℹ️ Про нас")
    markup.add(btn1, btn2)
    markup.add(btn3)
    return markup

# Кнопки міст
def cities_keyboard(cities_list):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttons = [types.KeyboardButton(city) for city in cities_list]
    buttons.append(types.KeyboardButton("🔙 На головне меню"))
    markup.add(*buttons)
    return markup

# НОВЕ: Кнопки "Оформити" або "Назад"
def order_decision_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("✅ Оформити замовлення")
    btn2 = types.KeyboardButton("🔙 Скасувати")
    markup.add(btn1, btn2)
    return markup