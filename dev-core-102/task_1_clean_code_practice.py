import time

basic_discount = 5.0 
loyal_customer_discount = 10.0 
is_loyal_customer = ["Antony","Bob","Daniel","Vanda","Tereza"]
customer_cart = {}
customer = input("Введите имя покупателя: ")
tax_sum = 18.0
wildcard_tax = 5.0

def products_price(price,count):
        return price * count
def try_loyal_customer(customer,is_loyal_customer):
     return customer in is_loyal_customer
while True:
    products = input("Введите название товара или (стоп) чтобы прекратить добавление товара в корзину: ")
    if products.lower() == "стоп":
        break
    
    
    try:
        price = float(input("Введите цену за единицу товара: "))
        count = float(input("Введите колличество товара: "))
        customer_cart[products] = float(products_price(price,count))
    except ValueError:
        print("Ошибка! Цена должна быть числом!")

total_price = sum(customer_cart.values())
try_loyal_customer(customer,is_loyal_customer)


def apply_discount(total_price, basic_discount, loyal_customer_discount, customer, is_loyal_customer):
    if try_loyal_customer(customer, is_loyal_customer):
         return  total_price - total_price / 100 * loyal_customer_discount
    else:
         return total_price - total_price / 100 * basic_discount
    
final_price_with_discount = apply_discount(total_price, basic_discount, loyal_customer_discount, customer, is_loyal_customer)

def apply_basic_tax(final_price_with_discount, tax_sum):
    return final_price_with_discount + final_price_with_discount * tax_sum / 100

final_price_with_tax = apply_basic_tax(final_price_with_discount, tax_sum)

current_minute = int(time.strftime("%M"))

def apply_wildcard_tax(wildcard_tax,final_price_with_tax,current_minute):
     if current_minute % 2 == 0:
          return final_price_with_tax
     else:
          return final_price_with_tax + final_price_with_tax * wildcard_tax / 100

final_price_with_wildcard_tax = apply_wildcard_tax(wildcard_tax,final_price_with_tax,current_minute)


def calculate_final_price(final_price_with_wildcard_tax,final_price_with_tax,final_price_with_discount,total_price,customer):
    return print(" Покупатель: ",customer,"\n Список продуктов: ",customer_cart,"\n Итоговая цена без учета скидок и НДС: ",total_price, "\n Цена с учетом скидки: ", final_price_with_discount, "\n Итоговая цена с учетом НДС:",final_price_with_tax, "\n Итоговая цена с учетом дополнительного налога: ",final_price_with_wildcard_tax, "\n Итого к оплате: ",final_price_with_wildcard_tax)

final_price = calculate_final_price(final_price_with_wildcard_tax,final_price_with_tax,final_price_with_discount,total_price,customer)
print(final_price)
