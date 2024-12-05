# Словари для хранения рецептов и цен на ингредиенты
recipes = {
    "Pasta": ["Tomatoes", "Cheese", "Spaghetti"],
    "Salad": ["Cucumbers", "Tomatoes", "Lettuce"],
    "Eggs": ["Bacon","Eggs","Mayonnaise"]
}

ingredient_prices = {
    "Tomatoes": 500,
    "Cheese": 2000,
    "Spaghetti": 1500,
    "Cucumbers": 300,
    "Lettuce": 700,
    "Bacon": 1000,
    "Eggs": 600,
    "Mayonnaise": 650
}

# Функция для отображения доступных рецептов и ингредиентов
def show_available_recipes():
    print("Доступные рецепты:")
    for recipe, ingredients in recipes.items():
        print(f"- {recipe}: {', '.join(ingredients)}")
    print("\nДоступные ингредиенты:")
    for ingredient, price in ingredient_prices.items():
        print(f"- {ingredient}: {price} тенге")

# Функция для добавления нового рецепта
def add_new_recipe():
    recipe_name = input("Введите название нового блюда: ")
    ingredients = input("Введите ингредиенты через запятую: ").split(",")
    
    # Убираем лишние пробелы в названиях ингредиентов
    ingredients = [ingredient.strip() for ingredient in ingredients]

    # Добавляем новый ингредиент и его цену, если нужно
    for ingredient in ingredients:
        if ingredient not in ingredient_prices:
            price = float(input(f"Введите стоимость нового ингредиента \"{ingredient}\": "))
            ingredient_prices[ingredient] = price

    recipes[recipe_name] = ingredients
    print(f"Рецепт {recipe_name} добавлен!")

# Функция для расчета стоимости рецепта
def calculate_recipe_cost():
    recipe_name = input("Введите название рецепта: ")
    
    if recipe_name not in recipes:
        print("Этот рецепт не существует.")
        return

    ingredients = recipes[recipe_name]
    total_cost = 0

    print(f"\nИнгредиенты для {recipe_name}:")
    for ingredient in ingredients:
        price = ingredient_prices[ingredient]
        print(f"- {ingredient}: {price} тенге")
        total_cost += price

    print(f"\nОбщая стоимость: {total_cost} тенге")
    
    # Применение скидки
    if total_cost > 30000:
        total_cost *= 0.9
        print(f"Итоговая стоимость с учетом скидки: {total_cost} тенге")
    else:
        print(f"Итоговая стоимость: {total_cost} тенге")

# Основная функция программы
def main():
    while True:
        show_available_recipes()
        print("\nВыберите действие:")
        print("1. Добавить новый рецепт")
        print("2. Рассчитать стоимость рецепта")
        print("3. Выйти")
        
        action = input("> ")

        if action == "1":
            add_new_recipe()
        elif action == "2":
            calculate_recipe_cost()
        elif action == "3":
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")

# Запуск программы
if __name__ == "__main__":
    main()
