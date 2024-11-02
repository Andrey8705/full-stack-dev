
basic_discount = 5.0 #Базовая скидка в 5 процентов
loyal_customer_discount = 10.0 #Дополнительная скидка для постоянных клиентов
is_loyal_customer = ["Antony","Bob","Daniel","Vanda","Tereza"]
quantity = ""
#loyal_customer = input("Введите имя покупателя: ")
customer_cart = {}


def products_price(price,count):
        return price * count

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



def apply_basic_discount(total_price, basic_discount):
    return "Базовая скидка применена! Вот итоговая сумма с учетом скидки 5%: ",total_price - total_price / 100 * basic_discount





#def apply_loyalty_discount(total,basic_discount,loyal_customer,loyal_customer_discount,is_loyal_customer):
 #   if loyal_customer in is_loyal_customer:
#        return ((total / 100) * (basic_discount + loyal_customer_discount)) , "Скидка для постоянного покупателя успешно применена!"
  #  else:
  #      return apply_basic_discount(total, basic_discount) , "Не является постоянным клиентом"




#def apply_basic_tax():
  #  return 



#def apply_wildcard_tax():
  #  return



#def calculate_final_price():
  #  return
print(" Итоговая сумма без учета скидки: ", total_price)
print (apply_basic_discount(total_price,basic_discount))

