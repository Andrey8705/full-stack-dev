active_recreation = { #Словарь с видами активного отдыха и ключами к ним.
    "Прыжки с парашютом": {"height": False},
    "Рыбалка": {"nature": True},
    "Скалолазанье": {"nature": True},
    "Охота": {"nature": True, "weapon": True},
    "Бильярд": {},
    "Сплав по горным рекам": {"nature": True, "swimming": True},
    "Поход в лес": {"nature": True},
    "Страйкбол": {"weapon": True},
}
passive_recreation = { #Словарь для пассивного отдыха с ключами.
    "Сон": {"perseverance": False},
    "Компьютерные игры": {"perseverance": True},
    "Лепка из глины": {"perseverance": True},
    "Медитация": {"perseverance": True},
    "Чтение книги": {"books": True},
    "Рисование": {"perseverance": True},
}


while True: #Будем требовать от пользователя правильного ввода пока он этого не сделает! Цикл на выбор вида отдыха
    type_of_holiday = input(
        "Выберите тип отдыха:\n1)Активный отдых\n2)Пассивный отдых\n"
    )
    if type_of_holiday == "1":
        print("Ваш выбор - активный отдых")
        break # Останавливаем цикл
    elif type_of_holiday == "2":
        print("Ваш выбор - пассивный отдых")
        break
    else:
        print("Ошибка ввода!Введите 1 или 2")


if type_of_holiday == "1": #Задаем вопросы в зависимости от выбранного вида отдыха
    print("Сейчас я задам несколько вопросов чтобы подобрать вам отдых по душе!")
    height = input("Вы боитесь высоты? Да/Нет: ").strip().lower() == "да"
    nature = input("Вы любите природу? Да/Нет: ").strip().lower() == "да"
    weapon = input("Вы любите оружие? Да/Нет: ").strip().lower() == "да"
    swimming = input("Вы умеете плавать? Да/Нет: ").strip().lower() == "да"
    perseverance = None
    books = None
elif type_of_holiday == "2":
    print("Сейчас я задам несколько вопросов чтобы подобрать вам отдых по душе!")
    perseverance = input("Вы усидчивы? Да/Нет: ").strip().lower() == "да"
    books = input("Вы любите книги? Да/Нет: ").strip().lower() == "да"
    height = None
    nature = None
    weapon = None
    swimming = None


def activity( #Основная логика программы.Функция проверяет на соответсвие ответы пользователя и ключи в словаре.
    type_of_holiday,
    height,
    swimming,
    weapon,
    nature,
    perseverance,
    books,
    active_recreation,
):
    suitable_activities = [] #Словарь с подходящими активностями
    if type_of_holiday == "1":
        for activity, conditions in active_recreation.items():
            if (
                ("height" not in conditions or conditions["height"] == height) #Проверка на соответствие. Если хоть одно условие не будет выполнено, занятие не подойдет.
                and ("swimming" not in conditions or conditions["swimming"] == swimming)
                and ("weapon" not in conditions or conditions["weapon"] == weapon)
                and ("nature" not in conditions or conditions["nature"] == nature)
            ):
                suitable_activities.append(activity)
    elif type_of_holiday == "2":
        for activity, conditions in passive_recreation.items():
            if (
                "perseverance" not in conditions
                or conditions["perseverance"] == perseverance
            ) and ("books" not in conditions or conditions["books"] == books):
                suitable_activities.append(activity)
    return suitable_activities


suitable_activities = activity( # Вызываем функцию
    type_of_holiday,
    height,
    swimming,
    weapon,
    nature,
    perseverance,
    books,
    active_recreation,
)


if suitable_activities: #Выводим результат
    print("Вам подходят следующие виды активного отдыха:")
    for activity in suitable_activities:
        print("-", activity)
else:
    print("К сожалению, мы не нашли подходящих вариантов.")
