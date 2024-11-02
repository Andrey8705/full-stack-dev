
price =""
basic_discount = 5 #Базовая скидка в 5 процентов
loyal_customer_discount = 10 #Дополнительная скидка для постоянных клиентов
is_loyal_customer = ["Antony","Bob","Daniel","Vanda","Tereza"]
total = 400
quantity = ""
loyal_customer = input("Введите имя покупателя: ")





def apply_basic_discount(total, basic_discount):
    return total / 100 * basic_discount , "Базовая скидка применена!"

print (apply_basic_discount(total,basic_discount))

def apply_loyalty_discount(total,basic_discount,loyal_customer,loyal_customer_discount,is_loyal_customer):
    if loyal_customer in is_loyal_customer:
        return ((total / 100) * (basic_discount + loyal_customer_discount)) , "Скидка для постоянного покупателя успешно применена!"
    else:
        return apply_basic_discount , "Не является постоянным клиентом"

apply_loyalty_discount(total,basic_discount,loyal_customer,loyal_customer_discount,is_loyal_customer)
print (apply_loyalty_discount(total,basic_discount,loyal_customer,loyal_customer_discount,is_loyal_customer))