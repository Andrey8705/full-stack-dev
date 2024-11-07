import os

# Путь к файлу для сохранения введённых пользователем данных
file_path = "user_info.txt"

# Функция для получения данных от пользователя
def get_user_info():
    name = input("Введите ваше имя: ")

    # Обработка ошибок для ввода возраста
    while True:
        try:
            age = int(input("Введите ваш возраст: "))
            break
        except ValueError:
            print("Пожалуйста, введите числовое значение для возраста.")

    # Обработка ошибок для ввода цвета (без чисел и специальных символов)
    while True:
        color = input("Введите ваш любимый цвет: ")
        if color.isalpha():  # Проверка, что введён только текст без чисел и специальных символов
            break
        else:
            print("Цвет не должен содержать цифр или специальных символов. Попробуйте снова.")

    return name, age, color

# Функция для сохранения информации в файл
def save_user_info(name, age, color):
    with open(file_path, "w") as file:
        file.write(f"Имя: {name}\nВозраст: {age}\nЛюбимый цвет: {color}")
    print("Информация успешно сохранена в файл user_info.txt.\n")

# Функция для чтения информации из файла
def read_user_info():
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            print("Сохранённая информация:")
            print(file.read())
    else:
        print("Файл с информацией не найден.\n")

# Основная функция программы
def main():
    name, age, color = get_user_info()

    # Вывод информации на экран
    print("\nВаши данные:")
    print(f"Имя: {name}\nВозраст: {age}\nЛюбимый цвет: {color}\n")

    # Сохранение информации в файл
    save_user_info(name, age, color)

    # Запрос на вывод информации из файла
    choice = input("Хотите ли вы прочитать сохранённые данные из файла? (да/нет): ").strip().lower()
    if choice == "да":
        read_user_info()
    else:
        print("Выход из программы.")

# Запуск программы
main()
