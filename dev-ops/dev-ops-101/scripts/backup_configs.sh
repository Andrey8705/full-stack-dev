#!/bin/bash

# Проверка SSH ключа и его добавление
if [ -f ~/.ssh/id_ed25519 ]; then
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_ed25519
else
    echo "SSH ключ не найден в ~/.ssh/id_ed25519"
    exit 1
fi

# Путь к директории для резервных копий
BACKUP_DIR=~/backup-ssh
CURRENT_DATE=$(date +"%Y%m%d")

# Создание директории для резервных копий с текущей датой
if ! mkdir -p "${BACKUP_DIR}/backup_${CURRENT_DATE}"; then
    echo "Ошибка при создании директории резервных копий"
    exit 1
fi

# Запрос имени файла для копирования
read -e -p "Введите имя файла для резервного копирования: " FILE_TO_BACKUP

# Проверка существования файла
if [ ! -f "$FILE_TO_BACKUP" ]; then
    echo "Файл $FILE_TO_BACKUP не существует."
    exit 1
fi

# Копирование файла в директорию резервных копий
cp "$FILE_TO_BACKUP" "$BACKUP_DIR/backup_$CURRENT_DATE/"

# Переход в директорию резервных копий
cd "$BACKUP_DIR" || exit

# Инициализация репозитория, если он еще не инициализирован
if [ ! -d .git ]; then
    git init
    # Явно создаем ветку main
    git checkout -b main
fi

# Проверка и добавление remote
if ! git remote | grep -q "origin"; then
    git remote add origin git@github.com:Andrey8705/backup-ssh.git
fi

# Добавление изменений в репозиторий
git add .
git commit -m "backups $CURRENT_DATE"

# Пуш с установкой upstream при необходимости
git push origin main || {
    echo "Попытка установить upstream..."
    git push --set-upstream origin main || {
        echo "Ошибка при пуше! Проверьте подключение к GitHub и права доступа."
        exit 1
    }
}

echo "Резервное копирование завершено и загружено в репозиторий."
