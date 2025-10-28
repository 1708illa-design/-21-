
requests         # Щоб отримувати дані з сайтів (наприклад, з Google, YouTube, API)
numpy            # Для математики: числа, масиви, обчислення
pandas           # Для таблиць: як Excel, але в Python
matplotlib       # Щоб малювати графіки (лінії, стовпчики тощо)
seaborn          # Ще красивіші графіки, ніж matplotlib
openpyxl         # Щоб читати і записувати Excel-файли (.xlsx)
pygame           # Для створення простих ігор з графікою і звуком
flask            # Щоб зробити свій сайт або веб-додаток
beautifulsoup4   # Щоб витягувати дані з HTML-сторінок (наприклад, новини з сайту)
pyttsx3          # Щоб озвучити текст голосом (працює без інтернету)




# Імпорт лише 5 бібліотек
import requests
import numpy as np
import pandas as pd
import datetime
import pyttsx3

#1️ Requests – отримання даних з вебу
try:
    response = requests.get("https://api.github.com")
    print("Requests : Статус відповіді =", response.status_code)
except Exception as e:
    print("Помилка у requests:", e)

#2️ NumPy – обчислення середнього значення
try:
    arr = np.array([5, 10, 15, 20])
    print("NumPy : Середнє значення =", np.mean(arr))
except Exception as e:
    print("Помилка у NumPy:", e)

#3️ Pandas – створення таблиці (DataFrame)
try:
    data = {'Імʼя': ['Ілля', 'Анна', 'Роман'], 'Оцінка': [90, 85, 95]}
    df = pd.DataFrame(data)
    print("Pandas :\n", df)
except Exception as e:
    print("Помилка у Pandas:", e)

#4️ Datetime - поточний час
try:
    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print("Datetime ✅: Поточна дата та час =", formatted_time)
except Exception as e:
    print("Помилка у datetime:", e)

#5️ pyttsx3 – озвучення тексту
try:
    engine = pyttsx3.init()
    engine.say("Hello Taras Anatoliyovich.")
    engine.runAndWait()
    print("pyttsx3 : текст озвучено")
except Exception as e:
    print("Помилка у pyttsx3:", e)



"""
try:	Запускає код, який може викликати помилку
except:	Виконується, якщо в try сталася помилка
Exception as e	Отримує інформацію про саму помилку
finally: (необов’язково)	Виконується завжди, навіть якщо була помилк
""" 
