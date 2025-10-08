def format_price(price):
    return f"{price:.2f} грн"

def check_availability(store, *items):
    return {item: store.get(item, [0, False]) for item in items}

def make_order(store):
    products = input("Введіть товари через пробіл: ").split()
    selected = check_availability(store, *products)

    unavailable = [name for name, data in selected.items() if not data[1]]

    if unavailable:
        print("Немає в наявності:", ", ".join(unavailable))
        return

    total = 0
    print("\nВаше замовлення:")
    for name, (price, _) in selected.items():
        print(f"{name}: {format_price(price)}")
        total += price

    print("Сума до сплати:", format_price(total))

def show_products(store):
    print("\nСписок товарів:")
    for name, (price, available) in store.items():
        status = "є в наявності" if available else "немає в наявності"
        print(f"{name}: {format_price(price)} ({status})")

def main():
    store = {
        "Хліб": [25, True],
        "Молоко": [36, True],
        "Сир": [120, False],
        "Яблука": [48, True],
        "Йогурт": [30, False]
    }

    while True:
        print("\n1 - Переглянути товари")
        print("2 - Зробити замовлення")


        choice = input("Ваш вибір: ")

        if choice == "1":
            show_products(store)
        elif choice == "2":
            make_order(store)
            print("Дякуємо за покупку!")
            break
        else:
            print("Невірна опція, спробуйте ще раз.")

if __name__ == "__main__":
    main()
