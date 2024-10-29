#!/bin/bash

echo "Выберите действие:"
echo "1) Обновление и апгрейд пакетов"
echo "2) Установка Nginx"
echo "3) Создание нового пользователя"
echo "4) Резервное копирование файлов"
echo "5) Выполнить все шаги"
read -p "Введите номер действия (1-5): " ACTION

case $ACTION in
    1)
        echo "Запуск обновления и апгрейда пакетов..."
        bash auto-update.sh
        ;;
    2)
        echo "Установка Nginx..."
        bash nginx.sh
        ;;
    3)
        echo "Создание нового пользователя..."
        bash users_create.sh
        ;;
    4)
        echo "Резервное копирование файлов..."
        bash backup_configs.sh
        ;;
    5)
        echo "Выполнение всех шагов..."
        bash auto-update.sh
        bash nginx.sh
        bash users_create.sh
        bash backup_configs.sh
        ;;
    *)
        echo "Неверный ввод. Пожалуйста, введите номер от 1 до 5."
        exit 1
        ;;
esac

echo "Выбранное действие выполнено успешно."
