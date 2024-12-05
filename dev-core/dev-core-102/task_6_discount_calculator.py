def apply_discount(price):
    return price * 0.9 if price > 100 else price


products = [] # Список продуктов

while True:
    user_input = input("Введите цену продукта (или 'стоп' для завершения): ").strip().lower()
    
    if user_input == "стоп":
        break  # Завершаем ввод, если пользователь вводит "стоп"
    
    try:
        price = float(user_input)
        products.append(price)
    except ValueError:
        print("Пожалуйста, введите числовое значение для цены.")

discounted_products = map(apply_discount, filter(lambda x: x > 100, products)) # Применение скидки для продуктов, стоимость которых больше 100


total_sum = sum(discounted_products) # Вычисление итоговой суммы с учетом скидок

# Вывод результата
print(f"Итоговая сумма покупок с учетом скидок: {total_sum:.2f}")
