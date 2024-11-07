# Кортеж для хранения координат места проведения конференции
conference_location = (55.7558, 37.6176)  # Пример координат (Москва, Россия)

# Словарь для хранения участников конференции
participants = {}

# Функция для добавления нового участника
def add_participant():
    name = input("Введите имя участника: ")
    age = input("Введите возраст участника: ")
    email = input("Введите e-mail участника: ")
    
    participants[name] = {
        'Имя': name,
        'Возраст': age,
        'E-mail': email
    }
    print(f"Участник {name} успешно добавлен.\n")

# Функция для удаления участника
def remove_participant():
    name = input("Введите имя участника, которого хотите удалить: ")
    if name in participants:
        del participants[name]
        print(f"Участник {name} успешно удален.\n")
    else:
        print(f"Участник с именем {name} не найден.\n")

# Функция для отображения информации о каждом участнике
def display_participants():
    if participants:
        print("Список участников конференции:")
        for name, info in participants.items():
            print(f"Имя: {info['Имя']}, Возраст: {info['Возраст']}, E-mail: {info['E-mail']}")
        print()  # Пустая строка для разделения выводов
    else:
        print("Список участников пуст.\n")

# Функция для отображения координат места проведения конференции
def display_conference_location():
    print(f"Координаты места проведения конференции: {conference_location}\n")

# Основная функция программы
def main():
    while True:
        print("Выберите действие:")
        print("1 - Добавить участника")
        print("2 - Удалить участника")
        print("3 - Просмотреть список участников")
        print("4 - Просмотреть координаты места проведения")
        print("5 - Выйти")
        
        choice = input("Ваш выбор: ")

        if choice == '1':
            add_participant()
        elif choice == '2':
            remove_participant()
        elif choice == '3':
            display_participants()
        elif choice == '4':
            display_conference_location()
        elif choice == '5':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите действие от 1 до 5.\n")

# Запуск программы
main()
