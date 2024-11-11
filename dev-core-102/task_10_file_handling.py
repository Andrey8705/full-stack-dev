import json
import os

# Функция для сохранения рецептов и цен на ингредиенты в файл
def save_data_to_file(recipes_filename="recipes.txt", prices_filename="ingredient_prices.txt"):
    try:
        # Сохраняем рецепты
        with open(recipes_filename, "w", encoding="utf-8") as file:
            json.dump(recipes, file, ensure_ascii=False, indent=4)
        
        # Сохраняем цены на ингредиенты
        with open(prices_filename, "w", encoding="utf-8") as file:
            json.dump(ingredient_prices, file, ensure_ascii=False, indent=4)

        print(f"Данные сохранены в файлы {recipes_filename} и {prices_filename}.")
    except Exception as e:
        print(f"Ошибка при сохранении данных в файлы: {e}")

# Функция для загрузки рецептов и цен на ингредиенты из файла
def load_data_from_file(recipes_filename="recipes.txt", prices_filename="ingredient_prices.txt"):
    global recipes, ingredient_prices
    if os.path.exists(recipes_filename) and os.path.exists(prices_filename):
        try:
            # Загружаем рецепты
            with open(recipes_filename, "r", encoding="utf-8") as file:
                recipes = json.load(file)
            
            # Загружаем цены на ингредиенты
            with open(prices_filename, "r", encoding="utf-8") as file:
                ingredient_prices = json.load(file)
            
            print(f"Данные загружены из файлов {recipes_filename} и {prices_filename}.")
        except Exception as e:
            print(f"Ошибка при загрузке данных из файлов: {e}")
    else:
        print(f"Один или оба файла {recipes_filename} и {prices_filename} не существуют.")

# Функция для отображения всех рецептов
def show_recipes():
    if recipes:
        print("\nРецепты:")
        for recipe, ingredients in recipes.items():
            print(f"- {recipe}: {', '.join(ingredients)}")
    else:
        print("Нет загруженных рецептов.")

# Функция для добавления нового рецепта
def add_new_recipe():
    recipe_name = input("Введите название нового блюда: ").strip()
    ingredients_input = input("Введите ингредиенты через запятую: ").strip().split(",")
    ingredients = [ingredient.strip() for ingredient in ingredients_input]

    # Запрашиваем стоимость каждого нового ингредиента
    for ingredient in ingredients:
        if ingredient not in ingredient_prices:
            price = float(input(f"Введите стоимость нового ингредиента \"{ingredient}\": ").strip())
            ingredient_prices[ingredient] = price
    
    # Добавляем новый рецепт
    recipes[recipe_name] = ingredients
    print(f"Рецепт \"{recipe_name}\" добавлен!")

# Функция для расчета стоимости рецепта
def calculate_recipe_cost(recipe_name):
    if recipe_name in recipes:
        ingredients = recipes[recipe_name]
        total_cost = 0
        print(f"\nИнгредиенты для {recipe_name}:")
        
        for ingredient in ingredients:
            if ingredient in ingredient_prices:
                price = ingredient_prices[ingredient]
                print(f"- {ingredient}: {price} тенге")
                total_cost += price
            else:
                print(f"Стоимость ингредиента {ingredient} не найдена.")
        
        print(f"\nОбщая стоимость: {total_cost} тенге")
        
        if total_cost > 30000:
            discount = 0.1 * total_cost
            print(f"Применена скидка 10%. Итоговая стоимость: {total_cost - discount} тенге")
        else:
            print(f"Итоговая стоимость без скидки: {total_cost} тенге")
    else:
        print(f"Рецепт \"{recipe_name}\" не найден.")

# Основная функция программы
def main():
    while True:
        print("\nВыберите действие:")
        print("1. Добавить новый рецепт")
        print("2. Рассчитать стоимость рецепта")
        print("3. Показать рецепты")
        print("4. Сохранить данные в файл")
        print("5. Загрузить данные из файла")
        print("6. Выйти")

        action = input("> ")

        if action == "1":
            add_new_recipe()
        elif action == "2":
            recipe_name = input("Введите название рецепта для расчета стоимости: ").strip()
            calculate_recipe_cost(recipe_name)
        elif action == "3":
            show_recipes()
        elif action == "4":
            save_data_to_file()
        elif action == "5":
            load_data_from_file()
        elif action == "6":
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите 1, 2, 3, 4, 5 или 6.")

# Запуск программы
if __name__ == "__main__":
    main()
