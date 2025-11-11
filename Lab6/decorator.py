# decorator.py

# Декоратор, який перевіряє тип поверненого значення функції
def check_return_type(expected_type):  # expected_type — тип, який ми очікуємо (int, str, list і т.д.)
    def decorator(func):  # func — це функція, яку ми декоруємо
        def wrapper(a, b):  # внутрішня функція, яка "обгортає" нашу основну
            result = func(a, b)  # викликаємо оригінальну функцію і зберігаємо результат

            # Перевіряємо, чи результат має правильний тип
            if not isinstance(result, expected_type):
                # Якщо тип не збігається — кидаємо помилку
                raise TypeError(
                    f"Помилка: функція '{func.__name__}' повинна повертати тип "
                    f"{expected_type.__name__}, але повернула {type(result).__name__}."
                )

            # Якщо все добре — виводимо підтвердження
            print(f"✅ Результат '{result}' має правильний тип {expected_type.__name__}")

            return result  # повертаємо результат, щоб функція працювала як звичайно

        return wrapper  # повертаємо обгортку
    return decorator  # повертаємо сам декоратор
