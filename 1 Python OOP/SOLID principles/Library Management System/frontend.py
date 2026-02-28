from backend import (
    Book,
    Library,
    LibraryService,
    JSONFileManagement,
    CSVFileManagement,
    EmailNotificationService,
    SMSNotificationService,
    ReportGenerator,
)

file_manager = CSVFileManagement()
notification_service = EmailNotificationService()

library = Library()
library_service = LibraryService(
    library=library,
    file_manager=file_manager,
    notification_service=notification_service,
)

report_generator = ReportGenerator()


# ====== CONSOLE UI ======

def print_menu():
    print("\n=== Library Management System ===")
    print("1. Add Book")
    print("2. Remove Book")
    print("3. Show Report")
    print("4. Save Library")
    print("5. Load Library")
    print("6. Exit")


def add_book():
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year = int(input("Year: ").strip())

    book = Book(title, author, year)
    message = library_service.add_book(book)
    print(message)


def remove_book():
    title = input("Title of book to remove: ").strip()

    books = library_service.get_all_books()
    for book in books:
        if book.title == title:
            message = library_service.remove_book(book)
            print(message)
            return

    print("Book not found.")


def show_report():
    report = report_generator.generate_report(library_service.get_all_books())
    print("\n" + report)


def save_library():
    filename = input("Filename: ").strip()
    message = library_service.save_library(filename)
    print(message)


def load_library():
    filename = input("Filename: ").strip()
    message = library_service.load_library(filename)
    print(message)


def main():
    while True:
        print_menu()
        choice = input("Choose option: ").strip()

        try:
            if choice == "1":
                add_book()
            elif choice == "2":
                remove_book()
            elif choice == "3":
                show_report()
            elif choice == "4":
                save_library()
            elif choice == "5":
                load_library()
            elif choice == "6":
                print("Goodbye.")
                break
            else:
                print("Invalid option.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
