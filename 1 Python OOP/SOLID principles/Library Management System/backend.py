from abc import ABC, abstractmethod
import json
import csv
from datetime import datetime
DEFAULT_CURRENT_YEAR = datetime.now().year


class Book:

    def __init__(self, title: str, author: str, year: int):

        if not isinstance(title, str):
            raise TypeError("Title must be a string")
        if not title.strip():
            raise ValueError("Title cannot be empty")
        if not isinstance(author, str):
            raise TypeError("Author must be a string")
        if not author.strip():
            raise ValueError("Author cannot be empty")
        if not isinstance(year, int):
            raise TypeError("Year must be an integer")
        if year < 0:
            raise ValueError("Year cannot be negative")
        if year > DEFAULT_CURRENT_YEAR + 1:
            raise ValueError("Year cannot be in the future")

        self.__title = title
        self.__author = author
        self.__year = year

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        if not value.strip():
            raise ValueError("Title cannot be empty")
        self.__title = value

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Author must be a string")
        if not value.strip():
            raise ValueError("Author cannot be empty")
        self.__author = value

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Year must be an integer")
        if value < 0:
            raise ValueError("Year cannot be negative")
        if value > DEFAULT_CURRENT_YEAR + 1:
            raise ValueError("Year cannot be in the future")
        self.__year = value

    def __hash__(self):
        return hash((self.__title, self.__author, self.__year))

    def __eq__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return (self.__title == other.__title and
                self.__author == other.__author and
                self.__year == other.__year)

    def __str__(self):
        return f"Book {self.__title} by {self.__author} ({self.__year})"

    def __repr__(self):
        return f"Book(title={self.__title}, author={self.__author}, year={self.__year})"


class Library:

    def __init__(self, books=None):
        if books is None:
            books = []
        if not isinstance(books, list):
            raise TypeError("Books must be a list")
        for book in books:
            if not isinstance(book, Book):
                raise TypeError("All items in books must be instances of Book")
        self.__books = list(books)

    @property
    def books(self):
        return self.__books

    @books.setter
    def books(self, value: list):
        if not isinstance(value, list):
            raise TypeError("Books must be a list")
        for book in value:
            if not isinstance(book, Book):
                raise TypeError("All items in books must be instances of Book")
        self.__books = list(value)

    def add_book(self, book: Book):
        if not isinstance(book, Book):
            raise TypeError("Book must be an instance of Book")
        self.__books.append(book)

    def remove_book(self, book: Book):
        if not isinstance(book, Book):
            raise TypeError("Book must be an instance of Book")
        if book not in self.__books:
            raise ValueError("Book not found in library")
        self.__books.remove(book)

    def __str__(self):
        return f"Library with {len(self.__books)} books"

    def __repr__(self):
        return f"Library(books={self.__books})"


class FileManagement(ABC):

    @abstractmethod
    def save_library(self, library: Library, filename: str):
        pass

    @abstractmethod
    def load_library(self, filename: str) -> Library:
        pass


class CSVFileManagement(FileManagement):

    def save_library(self, library: Library, filename: str):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Title', 'Author', 'Year'])
            for book in library.books:
                writer.writerow([book.title, book.author, book.year])

    def load_library(self, filename: str) -> Library:
        books = []
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                book = Book(
                    title=row['Title'], author=row['Author'], year=int(row['Year']))
                books.append(book)
        return Library(books=books)


class JSONFileManagement(FileManagement):

    def save_library(self, library: Library, filename: str):
        with open(filename, 'w') as jsonfile:
            json.dump([{'title': book.title, 'author': book.author,
                      'year': book.year} for book in library.books], jsonfile)

    def load_library(self, filename: str) -> Library:
        with open(filename, 'r') as jsonfile:
            data = json.load(jsonfile)
            books = [Book(title=item['title'], author=item['author'],
                          year=int(item['year'])) for item in data]
        return Library(books=books)


class NotificationService(ABC):

    @abstractmethod
    def send_notification(self, message: str):
        pass


class EmailNotificationService(NotificationService):

    def send_notification(self, message: str):
        return f"Sending email notification: {message}"


class SMSNotificationService(NotificationService):

    def send_notification(self, message: str):
        return f"Sending SMS notification: {message}"


class LibraryService:

    def __init__(self, library: Library, file_manager: FileManagement, notification_service: NotificationService):
        if not isinstance(library, Library):
            raise TypeError("Library must be an instance of Library")
        if not isinstance(file_manager, FileManagement):
            raise TypeError(
                "File manager must be an instance of FileManagement")
        if not isinstance(notification_service, NotificationService):
            raise TypeError(
                "Notification service must be an instance of NotificationService")
        self.__library = library
        self.__file_manager = file_manager
        self.__notification_service = notification_service

    def add_book(self, book: Book):
        self.__library.add_book(book)
        return self.__notification_service.send_notification(
            f"Book '{book.title}' added to library")

    def remove_book(self, book: Book):
        self.__library.remove_book(book)
        return self.__notification_service.send_notification(
            f"Book '{book.title}' removed from library")

    def load_library(self, filename: str):
        self.__library = self.__file_manager.load_library(filename)
        return self.__notification_service.send_notification(
            f"Library loaded from {filename}")

    def save_library(self, filename: str):
        self.__file_manager.save_library(self.__library, filename)
        return self.__notification_service.send_notification(
            f"Library saved to {filename}")

    def get_all_books(self):
        return self.__library.books

    def __str__(self):
        return f"LibraryService managing {len(self.__library.books)} books with {type(self.__file_manager).__name__} and {type(self.__notification_service).__name__}"

    def __repr__(self):
        return f"LibraryService(library={self.__library}, file_manager={self.__file_manager}, notification_service={self.__notification_service})"


class ReportGenerator:

    def generate_report(self, books: list) -> str:
        report = f"Library Report:\nTotal Books: {len(books)}\n"
        for book in books:
            report += f"- {book.title} by {book.author} ({book.year})\n"
        return report
