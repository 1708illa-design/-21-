from loader import bot
import handlers.admin_handlers  # <--- ДОДАЙ ЦЕЙ РЯДОК!
import handlers.user_handlers

if __name__ == "__main__":
    print("✅ Бот CARGO запущено! Успішної здачі лабораторної!")
    bot.infinity_polling()