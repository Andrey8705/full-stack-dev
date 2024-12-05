import time
import random

# Функция для расчёта итоговой суммы заказа
def calculate_total(order_amount, discount_code):
    # Применение скидки с вероятностью 50%
    if random.random() < 0.50:
        order_amount *= 0.9  # Скидка 10%
        print("Скидка 10% применена! Ты везунчик!")
    else:
        print("Скидка 10% начисляется с вероятностью 50%.\nМожет в другой раз повезёт)")

    # Применение дополнительной скидки при заказе больше 1000
    if order_amount > 1000:
        order_amount *= 0.95  # Дополнительная скидка 5%
        print("Дополнительная скидка за заказ свыше 1000: 5%")

    # Применение скидки по промокоду
    if discount_code.lower() == "студент":
        order_amount *= 0.95  # Скидка 5% по промокоду
        print("Скидка по промокоду студент: 5%")
    elif discount_code.lower() == "голодныйстудент":
        order_amount *= 0.05 #Скидка 95% если студент совсем голодный
        print("Ну если совсем голодный... \nСкидка по промокоду голодный студент: 95%")


    # Проверка чётности текущей минуты для налога
    current_minute = time.localtime().tm_min
    if current_minute % 2 != 0:
        order_amount *= 1.05  # Применение налога 5%
        print("Налог 5% применён, так как минута нечётная.")
    else:
        print("Налог не применён, так как минута чётная.")

    return order_amount

# Основная функция программы
def final():
    try:
        order_amount = float(input("Введите сумму заказа: "))

        discount_code = input("Введите промокод, если он у вас есть: ").strip()

        total_amount = calculate_total(order_amount, discount_code)
        
        print(f"Итоговая сумма к оплате: {total_amount:.2f} тенге.")

    except ValueError:
        print("Ошибка: Введите корректное числовое значение для суммы заказа.")

final()
