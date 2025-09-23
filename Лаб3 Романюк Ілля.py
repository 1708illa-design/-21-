

students = {}#словник для зберігання даних


print("Введіть ім'я студента та оцінку (1-12). Для завершення введіть 'stop'.")

while True: #  Безкінечний цикл для введення даних
    name = input("Ім'я студента: ").strip()  # Введення імені студента
    if name.lower() == "stop":  # Якщо користувач вводить "stop", вийти з циклу
        break

    try:
        grade = int(input("Оцінка: ").strip())  # Введення оцінки як числа
        if grade < 1 or grade > 12:
            # Якщо оцінка не в діапазоні 1–12, повідомити і повернутись на початок
            print("Оцінка має бути в межах від 1 до 12.")
            continue
        students[name] = grade        # Зберігаємо оцінку у словник: ім'я — ключ, оцінка — значення
    except ValueError:
        print("Оцінка має бути числом.") # Якщо оцінка — не число, вивести повідомлення і повернутись на початок
        continue


print("\nРезультати:") #  Після завершення введення, виводимо результати
for name, grade in students.items():
    # Виводимо ім’я студента та його оцінку
    print(f"{name}: {grade}")

# Обчислення статистики
grades = list(students.values())  # Отримуємо список усіх оцінок
average = sum(grades) / len(grades) if grades else 0  # Середній бал (if grades else 0 перевірка чи він не порожній

#Розподіл студентів по категоріях:
excellent = {name: grade for name, grade in students.items() if 10 <= grade <= 12}     # Відмінники (створеня нового списку
# з сиску студентів і сортіровка, проходимо по кожному стодунту та його оцінці
good = {name: grade for name, grade in students.items() if 7 <= grade <= 9}           # Хорошисти
satisfactory = {name: grade for name, grade in students.items() if 4 <= grade <= 6}   # Відстаючі
failed = {name: grade for name, grade in students.items() if 1 <= grade <= 3}         # Ті, хто не здав

# Вивід статистики
print("\nСтатистика:")
print(f"Середній бал групи: {average:.2f}")  # Вивід середнього бала з двома знаками після коми

# Вивід кількості відмінників і їх імен (якщо є)
print(f"Кількість відмінників (10-12): {len(excellent)} - {', '.join(excellent.keys()) if excellent else 'немає'}")
#excellent.keys() — отримує список імен (ключів) зі словника excellent. ', '.join(...) —
# об'єднує імена в один рядок через кому.  if excellent else 'немає' — умовний вираз:
# Якщо словник excellent не порожній → показує імена.

print(f"Кількість хорошистів (7-9): {len(good)}")  # Кількість хорошистів
print(f"Кількість відстаючих (4-6): {len(satisfactory)}")  # Кількість відстаючих (len рахує кількість елементів в рядку
print(f"Кількість тих, хто не здав (1-3): {len(failed)}")  # Кількість тих, хто не здав
