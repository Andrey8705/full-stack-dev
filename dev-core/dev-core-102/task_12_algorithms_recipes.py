import bisect

# Словарь с рецептами и их стоимостью
recipes = {
    "Борщ": 3000,
    "Плов": 2500,
    "Салат": 1500,
    "Бифштекс": 5000,
}

# Функция для сортировки рецептов по стоимости (пузырьковая сортировка)
def bubble_sort(recipes):
    recipes_list = list(recipes.items())
    n = len(recipes_list)
    
    for i in range(n):
        for j in range(0, n-i-1):
            if recipes_list[j][1] > recipes_list[j+1][1]:
                recipes_list[j], recipes_list[j+1] = recipes_list[j+1], recipes_list[j]
    return recipes_list

# Функция для бинарного поиска рецепта по стоимости
def binary_search(sorted_recipes, target_price):
    # sorted_recipes: отсортированный список рецептов
    # target_price: стоимость, которую мы ищем
    low, high = 0, len(sorted_recipes) - 1
    while low <= high:
        mid = (low + high) // 2
        if sorted_recipes[mid][1] == target_price:
            return sorted_recipes[mid][0]
        elif sorted_recipes[mid][1] < target_price:
            low = mid + 1
        else:
            high = mid - 1
    return None

# Функция для жадного выбора рецептов в рамках бюджета
def greedy_recipe_selection(recipes, budget):
    sorted_recipes = bubble_sort(recipes)
    selected_recipes = []
    total_cost = 0
    for recipe, price in sorted_recipes:
        if total_cost + price <= budget:
            selected_recipes.append(recipe)
            total_cost += price
    return selected_recipes

# Главная функция для взаимодействия с пользователем
def main():
    print("Доступные рецепты:")
    for recipe, price in recipes.items():
        print(f"{recipe} — {price} тг.")
    
    budget = int(input("Введите свой бюджет: "))
    
    # Сортировка рецептов по стоимости
    sorted_recipes = bubble_sort(recipes)
    print("\nСортировка рецептов по стоимости:", [recipe for recipe, _ in sorted_recipes])

    # Жадный алгоритм для выбора рецептов
    possible_recipes = greedy_recipe_selection(recipes, budget)
    print(f"Рецепты, которые вы можете приготовить: {possible_recipes}")
    
    # Ввод стоимости рецепта для бинарного поиска
    price_search = int(input("\nВведите стоимость для поиска рецепта (или 'стоп' для завершения): "))
    recipe_found = binary_search(sorted_recipes, price_search)
    
    if recipe_found:
        print(f"Рецепт с такой стоимостью: {recipe_found}")
    else:
        print("Рецепт с такой стоимостью не найден.")

# Запуск программы
main()
