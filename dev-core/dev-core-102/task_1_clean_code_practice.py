import time

basic_discount = 5.0
loyal_customer_discount = 10.0
is_loyal_customer = ["Antony", "Bob", "Daniel", "Vanda", "Tereza"]
customer_cart = {}  # Словарь в который записывается список продуктов (Название : цена)
customer = input("Введите имя покупателя: ")
tax_sum = 18.0  # Налог НДС
wildcard_tax = 5.0  # Налог по нечетным минутам


def products_price(price, count):
    return price * count


def try_loyal_customer(
    customer, is_loyal_customer
):  # Проверяем является ли покупатель постоянным клиентом
    return customer in is_loyal_customer


while True:  # Запускаем цикл пока ввод товаров не будет окончен.
    products = input(
        "Введите название товара или (стоп) чтобы прекратить добавление товара в корзину: "
    )
    if products.lower() == "стоп":
        break

    try:
        price = float(input("Введите цену за единицу товара: "))
        count = float(input("Введите колличество товара: "))
        customer_cart[products] = float(products_price(price, count))
    except ValueError:
        print("Ошибка! Цена или количество должны быть числом!")

total_price = sum(customer_cart.values())  # Суммируем все значения в словаре


def apply_discount(
    total_price, basic_discount, loyal_customer_discount, customer, is_loyal_customer
):  # Применяем скидку
    if try_loyal_customer(
        customer, is_loyal_customer
    ):  # Проверка на постоянного клиента
        return total_price - total_price / 100 * loyal_customer_discount
    else:  # Базовая скидка
        return total_price - total_price / 100 * basic_discount


final_price_with_discount = apply_discount(
    total_price, basic_discount, loyal_customer_discount, customer, is_loyal_customer
)


def apply_basic_tax(final_price_with_discount, tax_sum):  # Применяем базовый налог
    return final_price_with_discount + final_price_with_discount * tax_sum / 100


final_price_with_tax = apply_basic_tax(final_price_with_discount, tax_sum)

current_minute = int(time.strftime("%M"))  # Запрашиваем текущую минуту


def apply_wildcard_tax(wildcard_tax, final_price_with_tax, current_minute):
    if current_minute % 2 == 0:  # Проверяем четная минута или нечетная
        return final_price_with_tax  # Если четная - оставляем цену без дополнительного налога
    else:
        return (
            final_price_with_tax + final_price_with_tax * wildcard_tax / 100
        )  # Добавляем дополнительный налог


final_price_with_wildcard_tax = apply_wildcard_tax(
    wildcard_tax, final_price_with_tax, current_minute
)  # Итоговая цена


def calculate_final_price(
    final_price_with_wildcard_tax,
    final_price_with_tax,
    final_price_with_discount,
    total_price,
    customer,
):
    return print(
        " Покупатель: ",
        customer,
        "\n Список продуктов: ",
        customer_cart,
        "\n Итоговая цена без учета скидок и НДС: ",
        total_price,
        "\n Цена с учетом скидки: ",
        final_price_with_discount,
        "\n Итоговая цена с учетом НДС:",
        final_price_with_tax,
        "\n Итоговая цена с учетом дополнительного налога: ",
        final_price_with_wildcard_tax,
        "\n Итого к оплате: ",
        final_price_with_wildcard_tax,
    )


calculate_final_price(
    final_price_with_wildcard_tax,
    final_price_with_tax,
    final_price_with_discount,
    total_price,
    customer,
)  # Вызываем функцию и выводим результат на экран
