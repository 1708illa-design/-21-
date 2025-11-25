import os
from telebot import TeleBot
from dotenv import load_dotenv


# Завантажуємо змінні оточення
load_dotenv()

# Якщо з .env не читає, можеш залишити токен тут
token = os.getenv("TOKEN")

# Створюємо бота

bot = TeleBot(token)
