class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = True

    def display_info(self):
        status = "Доступна" if self.is_available else "Недоступна"
        print(f"\"{self.title}\" — {self.author} | Статус: {status}")


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def search_book_by_title(self, title):
        return [book for book in self.books if title.lower() in book.title.lower()]

    def list_available_books(self):
        print("Доступные книги в библиотеке:")
        for book in self.books:
            if book.is_available:
                book.display_info()

    def borrow_book(self, title, user):
        for book in self.books:
            if book.title.lower() == title.lower() and book.is_available:
                if len(user.borrowed_books) >= 3:
                    print(f"{user.name}, вы не можете взять более 3 книг одновременно.")
                    return
                book.is_available = False
                user.borrowed_books.append(book)
                print(f"Книга \"{book.title}\" успешно выдана {user.name}.")
                return
        print(f"Книга \"{title}\" недоступна или не найдена.")

    def return_book(self, title, user):
        for book in user.borrowed_books:
            if book.title.lower() == title.lower():
                book.is_available = True
                user.borrowed_books.remove(book)
                print(f"{user.name} вернул книгу \"{book.title}\".")
                return
        print(f"Книга \"{title}\" не найдена в списке взятых вами книг.")


class User:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.borrowed_books = []

    def display_borrowed_books(self):
        if self.borrowed_books:
            print(f"Список взятых книг пользователем {self.name}:")
            for book in self.borrowed_books:
                book.display_info()
        else:
            print(f"{self.name}, у вас нет взятых книг.")


# Пример работы программы
library = Library()
# Добавляем книги в библиотеку
library.add_book(Book("1984", "Джордж Оруэлл", "123-456-789"))
library.add_book(Book("Мастер и Маргарита", "Михаил Булгаков", "234-567-890"))
library.add_book(Book("Қыз Жібек", "Жүсіпбек Аймауытов", "345-678-901"))
library.add_book(Book("Абай жолы", "Мұхтар Әуезов", "456-789-012"))
library.add_book(Book("Преступление и наказание", "Федор Достоевский", "567-890-123"))

# Запуск интерфейса программы
def main():
    print("Добро пожаловать в библиотеку!")
    name = input("Введите ваше имя: ")
    user_id = input("Введите ваш ID: ")
    user = User(name, user_id)

    while True:
        print("\nВыберите действие:")
        print("1. Показать доступные книги")
        print("2. Взять книгу")
        print("3. Вернуть книгу")
        print("4. Показать взятые книги")
        print("5. Выйти")

        choice = input("Ваш выбор: ")

        if choice == "1":
            library.list_available_books()

        elif choice == "2":
            title = input(f"{user.name}, введите название книги, которую хотите взять (или 'стоп' для выхода): ")
            if title.lower() == "стоп":
                continue
            library.borrow_book(title, user)

        elif choice == "3":
            title = input(f"{user.name}, введите название книги, которую хотите вернуть (или 'стоп' для выхода): ")
            if title.lower() == "стоп":
                continue
            library.return_book(title, user)

        elif choice == "4":
            user.display_borrowed_books()

        elif choice == "5":
            print("Спасибо, что воспользовались нашей библиотекой!")
            break

        else:
            print("Ошибка: выберите корректный пункт меню.")

if __name__ == "__main__":
    main()
