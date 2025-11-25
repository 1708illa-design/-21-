import random
import os
from dotenv import load_dotenv
from loader import bot
from telebot import types
from keyboards.reply import main_menu, cities_keyboard, order_decision_keyboard
from keyboards.inline import website_keyboard
from data.services import (
    save_order, is_user_registered, register_new_user,
    get_user_info, update_user_bonuses,
    UKRAINE_CITIES, get_route_info, get_usd_rate
)

load_dotenv()
try:
    ADMIN_ID = int(os.getenv("ADMIN_ID"))
except:
    ADMIN_ID = None

user_cache = {}


# ========================
# 1. СТАРТ І РЕЄСТРАЦІЯ
# ========================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    if is_user_registered(chat_id):
        bot.send_message(chat_id, "👋 З поверненням у CargoBot!", reply_markup=main_menu())
    else:
        msg = bot.send_message(chat_id, "🚚 Вітаю! Введіть ваше ПІБ:")
        bot.register_next_step_handler(msg, reg_name)


def reg_name(message):
    user_cache[message.chat.id] = {'fullname': message.text}
    msg = bot.send_message(message.chat.id, "📞 Введіть ваш номер телефону:")
    bot.register_next_step_handler(msg, reg_phone)


def reg_phone(message):
    user_cache[message.chat.id]['phone'] = message.text
    msg = bot.send_message(message.chat.id, "🏠 Введіть ваше місто проживання:")
    bot.register_next_step_handler(msg, reg_address)


def reg_address(message):
    cid = message.chat.id
    user_cache[cid]['address'] = message.text

    new_user = {
        "user_id": cid,
        "username": message.from_user.username,
        "fullname": user_cache[cid]['fullname'],
        "phone": user_cache[cid]['phone'],
        "address": user_cache[cid]['address']
    }
    register_new_user(new_user)
    bot.send_message(cid, "✅ Реєстрація успішна!", reply_markup=main_menu())


# ========================
# 2. МЕНЮ ТА ІНФО
# ========================
@bot.message_handler(func=lambda m: m.text == "ℹ️ Про нас")
def info(message):
    bot.send_message(
        message.chat.id,
        "Ми використовуємо Google Maps API та курс НБУ для точних розрахунків.",
        reply_markup=website_keyboard()
    )


@bot.message_handler(func=lambda m: m.text == "👤 Мій кабінет")
def profile(message):
    user = get_user_info(message.chat.id)
    if not user: return bot.send_message(message.chat.id, "Помилка! Тисни /start")

    text = (
        f"👤 **ОСОБИСТИЙ КАБІНЕТ**\n"
        f"📛 {user['fullname']}\n"
        f"📦 Посилок: {user.get('total_orders', 0)}\n"
        f"💎 Бонуси: {user.get('bonus_points', 0)}\n"
        f"💡 *100 бонусів = Безкоштовна доставка*"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


@bot.message_handler(func=lambda m: m.text == "🔙 На головне меню")
def back(message):
    bot.send_message(message.chat.id, "Головне меню", reply_markup=main_menu())


# ========================
# 3. ЛОГІКА ЗАМОВЛЕННЯ
# ========================
@bot.message_handler(func=lambda m: m.text == "🚚 Розрахувати доставку")
def calc_start(message):
    if not is_user_registered(message.chat.id): return bot.send_message(message.chat.id, "/start спочатку")

    msg = bot.send_message(message.chat.id, "📍 Місто ВІДПРАВЛЕННЯ:",
                           reply_markup=cities_keyboard(UKRAINE_CITIES.keys()))
    bot.register_next_step_handler(msg, get_from)


def get_from(message):
    if message.text == "🔙 На головне меню": return back(message)
    if message.text not in UKRAINE_CITIES:
        msg = bot.send_message(message.chat.id, "⚠️ Оберіть місто з кнопок!")
        return bot.register_next_step_handler(msg, get_from)

    if message.chat.id not in user_cache: user_cache[message.chat.id] = {}
    user_cache[message.chat.id]['from'] = message.text

    msg = bot.send_message(message.chat.id, "🏁 Місто ОТРИМАННЯ:", reply_markup=cities_keyboard(UKRAINE_CITIES.keys()))
    bot.register_next_step_handler(msg, get_to)


def get_to(message):
    if message.text == "🔙 На головне меню": return back(message)
    if message.text not in UKRAINE_CITIES or message.text == user_cache[message.chat.id]['from']:
        msg = bot.send_message(message.chat.id, "⚠️ Оберіть інше місто!")
        return bot.register_next_step_handler(msg, get_to)

    user_cache[message.chat.id]['to'] = message.text
    msg = bot.send_message(message.chat.id, "⚖️ Вага вантажу (кг):", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_weight_precal)


def get_weight_precal(message):
    cid = message.chat.id
    if not message.text.isdigit():
        msg = bot.send_message(cid, "🔢 Тільки цифри!")
        return bot.register_next_step_handler(msg, get_weight_precal)

    weight = int(message.text)
    user_cache[cid]['weight'] = weight

    c_from = user_cache[cid]['from']
    c_to = user_cache[cid]['to']
    dist, method = get_route_info(c_from, c_to)

    rate = get_usd_rate()
    user_cache[cid]['temp_rate'] = rate

    price_usd_pure = (dist * 0.05) + (weight * 1.0)  # Чиста ціна в доларах
    final_price = int(price_usd_pure * rate)

    user = get_user_info(cid)
    bonuses = user.get('bonus_points', 0)
    note = ""

    price_display_usd = round(price_usd_pure, 2)  # Округляємо для краси

    if bonuses >= 100:
        final_price = 0
        price_display_usd = 0.0
        note = "\n🎉 **Можлива знижка 100% (Бонуси)**"

    user_cache[cid]['temp_price'] = final_price

    text = (
        f"📋 **ПОПЕРЕДНІЙ РОЗРАХУНОК**\n"
        f"📍 {c_from} ➡️ {c_to}\n"
        f"🛣 {dist} км\n"
        f"💲 Курс: {rate}\n"
        f"💰 **СУМА: {final_price} грн / {price_display_usd} $**\n"  # <--- ЗМІНА ТУТ
        f"{note}\n\n"
        f"👇 **Бажаєте викликати кур'єра?**"
    )
    msg = bot.send_message(cid, text, parse_mode="Markdown", reply_markup=order_decision_keyboard())
    bot.register_next_step_handler(msg, handle_decision)


def handle_decision(message):
    cid = message.chat.id
    if message.text == "🔙 На головне меню":
        return back(message)

    if message.text == "✅ Оформити замовлення":
        msg = bot.send_message(cid,
                               f"✍️ Введіть **Вулицю та будинок** у м. {user_cache[cid]['from']} (звідки забрати):",
                               reply_markup=types.ReplyKeyboardRemove(), parse_mode="Markdown")
        bot.register_next_step_handler(msg, get_pickup)
    else:
        msg = bot.send_message(cid, "Натисніть кнопку 👇")
        bot.register_next_step_handler(msg, handle_decision)


def get_pickup(message):
    cid = message.chat.id
    user_cache[cid]['pickup_addr'] = message.text
    msg = bot.send_message(cid, f"✍️ Введіть **Вулицю та будинок** у м. {user_cache[cid]['to']} (куди доставити):",
                           parse_mode="Markdown")
    bot.register_next_step_handler(msg, get_delivery_final)


def get_delivery_final(message):
    cid = message.chat.id
    try:
        # Перевірка наявності даних розрахунку
        if cid not in user_cache or 'temp_price' not in user_cache[cid]:
            bot.send_message(cid, "⚠️ Дані застаріли. Будь ласка, почніть розрахунок заново: /start")
            return

        delivery_addr = message.text

        # Відновлюємо дані з кешу
        c_from = user_cache[cid]['from']
        c_to = user_cache[cid]['to']
        price = user_cache[cid]['temp_price']
        weight = user_cache[cid]['weight']
        pickup = user_cache[cid].get('pickup_addr', 'Самовивіз')
        rate = user_cache[cid].get('temp_rate', 42.0)

        # === ВИПРАВЛЕННЯ ПОМИЛКИ 'fullname' ===
        # Якщо в кеші немає імені (бо перезапустили бота), беремо з бази
        if 'fullname' in user_cache[cid]:
            fullname = user_cache[cid]['fullname']
        else:
            # Страховка: тягнемо з файлу users.json
            u_info = get_user_info(cid)
            fullname = u_info['fullname'] if u_info else "Невідомий клієнт"
        # ======================================

        # Перераховуємо долари
        val_usd = round(price / rate, 2) if price > 0 else 0.0

        order_id = random.randint(100000, 999999)
        spent = 100 if price == 0 else 0
        earned = update_user_bonuses(cid, spent)

        client_msg = (
            f"✅ **ЗАМОВЛЕННЯ #{order_id} ПРИЙНЯТО!**\n"
            f"➖➖➖➖➖➖➖➖\n"
            f"📤 **Звідки:** {c_from}, {pickup}\n"
            f"📥 **Куди:** {c_to}, {delivery_addr}\n"
            f"⚖️ Вага: {weight} кг\n"
            f"💰 **СУМА: {price} грн / {val_usd} $**\n"
            f"➖➖➖➖➖➖➖➖\n"
            f"💎 Нараховано бонусів: +{earned}\n"
            f"📞 _Чекайте дзвінка кур'єра._"
        )

        admin_msg = (
            f"🚨 **НОВЕ ЗАМОВЛЕННЯ #{order_id}**\n"
            f"👤 Клієнт: {fullname}\n"
            f"📱 Тел: `{user_cache[cid].get('phone', 'Не вказано')}`\n"
            f"📍 Маршрут: {c_from} -> {c_to}\n"
            f"💰 Сума: {price} грн"
        )

        save_order({"id": order_id, "user_id": cid, "price": price, "route": f"{c_from}-{c_to}"})

        bot.send_message(cid, client_msg, parse_mode="Markdown", reply_markup=main_menu())

        if ADMIN_ID:
            try:
                bot.send_message(ADMIN_ID, admin_msg, parse_mode="Markdown")
            except:
                pass

    except Exception as e:
        # Виводимо помилку в чат, щоб розуміти, що сталось
        bot.send_message(cid, f"🆘 Виникла помилка: {e}")
        print(f"ERROR: {e}")  # І в консоль