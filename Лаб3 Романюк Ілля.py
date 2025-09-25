# Створюємо порожній словник для збереження результатів студентів
results = {}
# Безкінечний цикл для введення даних
while True:
    name = input("Введіть ім'я: ")
    if name == "stop":
        break
    # Введення оцінки з перевіркою правильності
    while True:
        grade_in = input("Введіть оцінку  ")
        if grade_in:  # Перевіряємо, чи це число
            grade = int(grade_in)
            if 1 <= grade <= 12:
                results[name] = grade
                break
            else:
                print("Оцінка має бути від 1 до 12. Спробуйте ще раз.")
        else:
            print("Оцінка має бути числом. Спробуйте ще раз.")
#Виводимо список усіх студентів та їхні оцінки
if results:
    print("\nСписок студентів та їх оцінки:")
    for name, grade in results.items():
        print(f"{name}: {grade}")
        # Обчислюємо та виводимо середній бал
    print("Середній бал:", round(sum(results.values()) / len(results), 2))
# Класифікуємо студентів за рівнем успішності
    exelent = [n for n in results if 10 <= results[n] <= 12]
    good = [n for n in results if 7 <= results[n] <= 9]
    weak = [n for n in results if 4 <= results[n] <= 6]
    fail = [n for n in results if 1 <= results[n] <= 3]
# Виводимо кількість і список студентів у кожній категорії
    print("Відмінники:", len(exelent), "→", ', '.join(exelent) if exelent else "немає")
    print("Хорошисти:", len(good), "→", ', ')
    print("Відстаючі:", len(weak), "→", ', ')
    print("Не здали:", len(fail), "→", ', ')
else:
    print("Жодного студента не було введено.")
