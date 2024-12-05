import sympy as sp
# Имортируем модуль sp из библиотеки sympy
def calcfunction(convert_str):
    try:
        # Идёт конвертация строки введенной пользователем в математическое выражение
        convert = sp.sympify(convert_str)
        
        # Вычисление результата
        result = convert.evalf()
        
        # Проверка на наличие 'zoo' Так обозначается деление на ноль в библиотеке sympy
        if result == sp.zoo:
            return "Ошибка: деление на ноль!"
        return result
    #Проверка на корректность введенного выражения.
    except sp.SympifyError:
        return "Некорректное выражение!"

# Ввод от пользователя
user = input("Введите математическое выражение: ")
result = calcfunction(user)
print(f"Результат: {result}")
