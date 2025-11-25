import random


# --- КРОК 1: Створення файлу ---
def create_random_text_file(filename):
    """
    Створює файл із випадковим набором слів.
    100+ рядків, 100+ символів у рядку.
    """
    # Українські літери для генерації
    letters = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
    # Додаємо багато пробілів у набір, щоб формувалися "слова"
    population = letters + ' ' * 6

    with open(filename, 'w', encoding='utf-8') as f:
        for _ in range(101):  # Робимо 101 рядок (більше 100)
            # Генеруємо рядок зі 105 символів
            line = ''.join(random.choice(population) for _ in range(105))
            f.write(line + '\n')

    print(f"[INFO] Файл '{filename}' успішно створено.")


# --- КРОК 2: Генератор (Основне завдання) ---
def pair_counter_generator(filename):
    """
    Генератор:
    1. Читає файл рядок за рядком (економить пам'ять).
    2. Обирає 3 пари букв для пошуку.
    3. Рахує їх кількість, ігноруючи стики слів.
    """
    # Список можливих пар для пошуку
    all_pairs = ['ан', 'ун', 'ну', 'не', 'на', 'за', 'по', 'ми']

    with open(filename, 'r', encoding='utf-8') as f:
        line_num = 1
        for line in f:
            # Розбиваємо рядок на слова (split прибирає пробіли і enter)
            # Це вирішує проблему стику слів: "слово закінчується на у, наступне на н"
            # Вони стануть окремими елементами списку, і пара 'ун' не зарахується.
            words = line.split()

            # Вибираємо 3 випадкові пари для цього рядка (як в умові "в кожного різні")
            # Або можна брати фіксовані, якщо умова дозволяє. Тут беремо випадкові 3.
            target_pairs = random.sample(all_pairs, 3)

            # Рахуємо входження
            results = {}
            for pair in target_pairs:
                count = 0
                for word in words:
                    # Рахуємо пару ТІЛЬКИ всередині слова
                    count += word.count(pair)
                results[pair] = count

            # yield "випльовує" результат і чекає наступного виклику
            yield f"Рядок {line_num}: шукали {target_pairs} -> знайшли {results}"

            line_num += 1


# --- КРОК 3: Запуск ---
if __name__ == '__main__':
    file_name = 'lab9_text.txt'

    # 1. Створюємо файл
    create_random_text_file(file_name)

    print("-" * 50)
    print("Результати роботи генератора:")

    # 2. Створюємо об'єкт генератора
    my_gen = pair_counter_generator(file_name)

    # 3. Виводимо перші 10 результатів, щоб не засмічувати консоль
    # (або можна пройтись циклом по всьому генератору)
    for i in range(10):
        try:
            print(next(my_gen))
        except StopIteration:
            break