# main.py

# Імпортуємо наш декоратор із іншого файлу
from decorator import check_return_type

# Приклад 1 — функція повинна повертати ціле число (int)
@check_return_type(int)
def add(a, b):
    return a + b  # результат буде типу int

# Приклад 2 — функція повинна повертати рядок (str)
@check_return_type(str)
def make_string(a, b):
    return str(a + b)  # результат буде типу str

# Приклад 3 — функція навмисно повертає не той тип
@check_return_type(list)
def wrong_func(a, b):
    return a + b  # тут повертається число (int), а не список → буде помилка

# Точка входу програми
if __name__ == '__main__':
    # Викликаємо першу функцію — тип правильний ✅
    add(2, 3)

    # Викликаємо другу — тип теж правильний ✅
    make_string(4, 5)

    # Викликаємо третю — тип неправильний ❌
    try:
        wrong_func(1, 2)
    except TypeError as e:
        print(e)  # Виведе повідомлення про помилку
