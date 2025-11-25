import os
from telebot import types
from loader import bot
from dotenv import load_dotenv
from data.services import get_global_stats

load_dotenv()
# Спробуємо завантажити ID, якщо помилка - буде None
try:
    ADMIN_ID = int(os.getenv("ADMIN_ID"))
except:
    ADMIN_ID = None


def is_admin(user_id):
    return user_id == ADMIN_ID


@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if not is_admin(message.chat.id): return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📊 Статистика")
    btn2 = types.KeyboardButton("📥 Скачати базу")
    btn3 = types.KeyboardButton("🔙 Вихід")
    markup.add(btn1, btn2)
    markup.add(btn3)

    bot.send_message(message.chat.id, "🕵️‍♂️ **Адмін-Панель**", reply_markup=markup, parse_mode="Markdown")


@bot.message_handler(func=lambda m: m.text == "📊 Статистика")
def show_stats(message):
    if not is_admin(message.chat.id): return
    c, m, u = get_global_stats()
    text = (
        f"📊 **ФІНАНСОВИЙ ЗВІТ**\n"
        f"👥 Всього клієнтів: **{u}**\n"
        f"📦 Всього замовлень: **{c}**\n"
        f"💰 Загальний дохід: **{m} грн**"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


@bot.message_handler(func=lambda m: m.text == "📥 Скачати базу")
def download_db(message):
    if not is_admin(message.chat.id): return

    if os.path.exists("data/orders.json"):
        with open("data/orders.json", "rb") as f:
            bot.send_document(message.chat.id, f, caption="📂 База замовлень")
    else:
        bot.send_message(message.chat.id, "База порожня.")


@bot.message_handler(func=lambda m: m.text == "🔙 Вихід")
def admin_exit(message):
    if not is_admin(message.chat.id): return
    # Імпорт всередині функції, щоб уникнути помилок кругового імпорту
    from keyboards.reply import main_menu
    bot.send_message(message.chat.id, "Режим адміна вимкнено.", reply_markup=main_menu())