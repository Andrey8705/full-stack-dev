def get_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Ошибка: введите положительное число.")
            else:
                return value
        except ValueError:
            print("Ошибка: введите корректное число.")

def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Ошибка: введите положительное число.")
            else:
                return value
        except ValueError:
            print("Ошибка: введите корректное число.")

def main():
    total_sum = 0
    num_products = get_positive_integer("Введите количество продуктов (целое положительное число): ")

    if num_products == 0:
        print("Вы не добавили продукты в заказ.")
        return

    for i in range(1, num_products + 1):
        print(f"\nПродукт {i}:")
        quantity = get_positive_integer("Введите количество данного продукта: ")
        price_per_item = get_positive_float("Введите цену за единицу данного продукта: ")
        total_sum += quantity * price_per_item

    print(f"\nОбщая сумма заказа: {total_sum:.2f} тенге")

if __name__ == "__main__":
    main()
