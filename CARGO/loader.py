import os
from telebot import TeleBot
from dotenv import load_dotenv

# === ХАК ДЛЯ ВИПРАВЛЕННЯ ПОМИЛКИ ПІДКЛЮЧЕННЯ ===
# Це змушує Python ігнорувати системні проксі Windows,
# які часто викликають TimeoutError
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['NO_PROXY'] = '*'
# ===============================================

# Завантажуємо змінні оточення
load_dotenv()

# Якщо з .env не читає, можеш залишити токен тут
token = os.getenv("TOKEN")

# Створюємо бота
bot = TeleBot(token)