import os
import shutil

# Функция для вывода структуры каталогов и файлов
def print_directory_structure(path, level=0):
    """Рекурсивно выводит структуру файлов и папок в заданной директории"""
    try:
        # Получаем список всех файлов и папок в текущей директории
        items = os.listdir(path)
        
        for item in items:
            # Формируем полный путь к элементу (файл или папка)
            item_path = os.path.join(path, item)
            
            # Если элемент — это директория, выводим её и рекурсивно вызываем функцию для неё
            if os.path.isdir(item_path):
                print("  " * level + f"[DIR] {item}")
                print_directory_structure(item_path, level + 1)  # Рекурсивный вызов
            else:
                # Если это файл, просто выводим его
                print("  " * level + f"[FILE] {item}")
    except PermissionError:
        print("Нет доступа к одной из директорий.")
    except FileNotFoundError:
        print("Директория не найдена.")
        
# Функция для поиска файла по имени
def search_file(path, filename):
    """Рекурсивно ищет файл с заданным именем в директории и её поддиректориях"""
    try:
        # Получаем список всех файлов и папок в текущей директории
        items = os.listdir(path)
        
        for item in items:
            # Формируем полный путь к элементу
            item_path = os.path.join(path, item)
            
            # Если найден файл с нужным именем, возвращаем его полный путь
            if os.path.isfile(item_path) and item == filename:
                return item_path
            
            # Если это директория, рекурсивно ищем в ней
            if os.path.isdir(item_path):
                result = search_file(item_path, filename)
                if result:  # Если файл найден в поддиректории
                    return result
        return None  # Если файл не найден
    except PermissionError:
        print("Нет доступа к одной из директорий.")
    except FileNotFoundError:
        print("Директория не найдена.")
        
# Функция для подсчета общего размера файлов в директории
def calculate_total_size(path):
    """Рекурсивно подсчитывает общий размер файлов в директории"""
    total_size = 0
    try:
        # Получаем список всех файлов и папок в текущей директории
        items = os.listdir(path)
        
        for item in items:
            item_path = os.path.join(path, item)
            
            # Если это файл, добавляем его размер
            if os.path.isfile(item_path):
                total_size += os.path.getsize(item_path)
            
            # Если это директория, рекурсивно считаем её размер
            elif os.path.isdir(item_path):
                total_size += calculate_total_size(item_path)
        
        return total_size
    except PermissionError:
        print("Нет доступа к одной из директорий.")
    except FileNotFoundError:
        print("Директория не найдена.")
        
# Функция для копирования файлов из одной директории в другую
def copy_files(src, dst):
    """Рекурсивно копирует файлы и папки из одной директории в другую"""
    try:
        # Проверяем, существует ли директория назначения, если нет, создаем
        if not os.path.exists(dst):
            os.makedirs(dst)
        
        # Получаем список всех файлов и папок в исходной директории
        items = os.listdir(src)
        
        for item in items:
            item_path = os.path.join(src, item)
            destination_path = os.path.join(dst, item)
            
            # Если это файл, копируем его
            if os.path.isfile(item_path):
                shutil.copy(item_path, destination_path)
            
            # Если это директория, рекурсивно копируем её содержимое
            elif os.path.isdir(item_path):
                copy_files(item_path, destination_path)
    except PermissionError:
        print("Нет доступа к одной из директорий.")
    except FileNotFoundError:
        print("Директория не найдена.")
        
# Демонстрация работы программы
if __name__ == "__main__":
    # Путь к тестовой директории
    path = "D:/Microsoft VS Code"
    
    # 1. Печать структуры папок и файлов
    print("Структура директории:")
    print_directory_structure(path)
    
    # 2. Поиск файла в директории и поддиректориях
    filename_to_search = "example.txt"
    result = search_file(path, filename_to_search)
    if result:
        print(f"\nФайл найден: {result}")
    else:
        print(f"\nФайл '{filename_to_search}' не найден.")
    
    # 3. Подсчет общего размера файлов в директории
    total_size = calculate_total_size(path)
    print(f"\nОбщий размер файлов в директории: {total_size} байт.")
    
    # 4. Копирование файлов из одной директории в другую
    #source_dir = "source_folder"
    #destination_dir = "destination_folder"
    #copy_files(source_dir, destination_dir)
    #print(f"\nФайлы из '{source_dir}' были успешно скопированы в '{destination_dir}'.")
