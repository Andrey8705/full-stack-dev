#!/bin/bash

# Функция для логирования с временной меткой
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# Проверка на root-права
if [ "$EUID" -ne 0 ]; then
    log_message "Пожалуйста, запустите скрипт с правами суперпользователя (sudo)"
    exit 1
fi

log_message "Начинаем установку Nginx..."

# Обновление списка пакетов
log_message "Обновление списка пакетов..."
apt update -y

# Установка Nginx
log_message "Установка Nginx..."
apt install nginx -y

# Запуск службы Nginx
log_message "Запуск Nginx..."
systemctl start nginx

# Включение автозапуска Nginx при загрузке системы
log_message "Включение автозапуска Nginx..."
systemctl enable nginx

# Проверка статуса службы Nginx
log_message "Проверка статуса Nginx..."
if systemctl is-active --quiet nginx; then
    log_message "Nginx успешно установлен и работает."
else
    log_message "Произошла ошибка: служба Nginx не запущена."
    exit 1
fi

log_message "Установка и проверка Nginx завершены."

