import numpy as np
import requests

array_size = 10  # Размер массива
random_numbers = np.random.randint(1, 100, size=array_size)  # Массив случайных чисел от 1 до 99
print("Случайные числа:", random_numbers)

# Шаг 2: Отправляем массив на API
url = "https://httpbin.org/post"  # Тестовый API для POST-запросов
data = {
    "numbers": random_numbers.tolist()  # Преобразуем массив в список, чтобы отправить JSON
}

response = requests.post(url, json=data)  # Отправляем POST-запрос с данными
if response.status_code == 200:
    print("Ответ от сервера:", response.json())  # Показываем ответ сервера
else:
    print("Ошибка:", response.status_code)
