from telebot import types

def website_keyboard():
    markup = types.InlineKeyboardMarkup()
    # Тут кнопка посилання (URL)
    btn = types.InlineKeyboardButton("🌐 Відвідати наш сайт", url="https://google.com")
    markup.add(btn)
    return markup