import time

def user_request():
    return input("Введите URL: ")

def server_response(request):
    return f"Ожидание ответа от - {request}"

def main():
    request = user_request()
    print(f"Клиент отправил запрос {request} на сервер")
    time.sleep(1)

    response = server_response(request)
    print(response)
    time.sleep(1)

    # Имитация ошибки подключения
    print(f"Не удалось подключиться к {request}")
    time.sleep(0.5)
    print("Попробуйте ввести URL адрес не в терминал, а в специальную строку в браузере.")

# Запускаем программу
main()
