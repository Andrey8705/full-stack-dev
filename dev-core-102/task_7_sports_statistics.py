# Функция для вычисления итогового результата команды
def calculate_team_performance(results):
    wins = results.count("win")
    total_matches = len(results)
    
    # Применяем бонус, если команда выиграла больше половины матчей
    team_performance = wins / total_matches
    if team_performance > 0.5:
        team_performance += 0.1  # Бонус за хорошие результаты
    
    return team_performance

# Функция для расчета среднего результата игрока
def player_performance(scores):
    total_points = sum(scores)
    total_matches = len(scores)
    
    # Рассчитываем средний результат игрока
    avg_performance = total_points / total_matches
    
    # Применяем бонус, если игрок набрал больше 30 очков в одном из матчей
    if any(score > 30 for score in scores):
        avg_performance += 5  # Бонус за высокие очки в одном из матчей
    
    return avg_performance

# Функция для расчета итогового отчета команды
def final_report(team_results, player_avg_scores):
    # Оценка команды
    team_performance = calculate_team_performance(team_results)
    
    # Средний результат по всем игрокам
    avg_player_score = sum(player_avg_scores) / len(player_avg_scores)
    
    # Итоговая оценка команды
    overall_performance = (team_performance + avg_player_score) / 2
    
    if overall_performance >= 0.7:
        print("Отличная команда")
    else:
        print("Есть над чем работать")
    
    # Также выводим детали
    print(f"Командный результат: {team_performance:.2f}")
    print(f"Средний результат игроков: {avg_player_score:.2f}")
    print(f"Итоговое выступление: {overall_performance:.2f}")

# Пример использования программы
team_results = ["win", "lose", "win", "win", "lose"]  # Результаты команды (победы/поражения)
player_scores = [
    [25, 28, 32, 22],  # Результаты игрока 1 по матчам
    [30, 35, 28, 27],  # Результаты игрока 2 по матчам
    [15, 20, 18, 10]   # Результаты игрока 3 по матчам
]

# Рассчитываем средние результаты игроков
player_avg_scores = [player_performance(scores) for scores in player_scores]

# Генерируем финальный отчет
final_report(team_results, player_avg_scores)
