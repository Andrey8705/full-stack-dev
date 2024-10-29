#!/bin/bash

# Название лог-файла
LOG_FILE="/var/log/auto_update.log"

# Функция для логирования с временной меткой
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log_message "Начало обновления пакетов"

# Обновление списка пакетов
log_message "Обновление списка пакетов..."
if apt update -y >> "$LOG_FILE" 2>&1; then
    log_message "Список пакетов обновлен успешно"
else
    log_message "Ошибка при обновлении списка пакетов"
    exit 1
fi

# Установка обновлений и апгрейд пакетов
log_message "Установка обновлений..."
if apt upgrade -y >> "$LOG_FILE" 2>&1; then
    log_message "Обновления установлены успешно"
else
    log_message "Ошибка при установке обновлений"
    exit 1
fi

# Опционально: очистка ненужных пакетов
log_message "Очистка ненужных пакетов..."
if apt autoremove -y >> "$LOG_FILE" 2>&1; then
    log_message "Очистка завершена успешно"
else
    log_message "Ошибка при очистке ненужных пакетов"
fi

log_message "Обновление завершено"

