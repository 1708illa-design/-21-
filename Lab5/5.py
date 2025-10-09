# Імпорт лише 5 бібліотек
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyttsx3

# 1️⃣ Requests – отримання даних з вебу
try:
    response = requests.get("https://api.github.com")
    print("Requests ✅: Статус відповіді =", response.status_code)
except Exception as e:
    print("Помилка у requests:", e)

# 2️⃣ NumPy – обчислення середнього значення
try:
    arr = np.array([5, 10, 15, 20])
    print("NumPy ✅: Середнє значення =", np.mean(arr))
except Exception as e:
    print("Помилка у NumPy:", e)

# 3️⃣ Pandas – створення таблиці (DataFrame)
try:
    data = {'Імʼя': ['Ілля', 'Анна', 'Роман'], 'Оцінка': [90, 85, 95]}
    df = pd.DataFrame(data)
    print("Pandas ✅:\n", df)
except Exception as e:
    print("Помилка у Pandas:", e)

# 4️⃣ Matplotlib – побудова простого графіка
try:
    plt.plot([1, 2, 3], [2, 4, 1])
    plt.title("Графік приклад")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig("grafik.png")
    print("Matplotlib ✅: графік збережено у файл grafik.png")
except Exception as e:
    print("Помилка у Matplotlib:", e)

# 5️⃣ pyttsx3 – озвучення тексту
try:
    engine = pyttsx3.init()
    engine.say("Hello world is pyttsx3.")
    engine.runAndWait()
    print("pyttsx3 ✅: текст озвучено")
except Exception as e:
    print("Помилка у pyttsx3:", e)
