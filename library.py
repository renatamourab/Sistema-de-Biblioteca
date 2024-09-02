from typing import List

from models.book import Book
from notifiers.book_availability_notifier import BookAvailabilityNotifier


class Library:

    def __init__(self):

        from adapters.external_catalog_adapter import ExternalDataBank
        from models.book import Book
        from models.loan import Loan
        from models.user import User
        
        self.books: List[Book] = ConfigurationManager().catalog_books()
        self.users: List[User] = []
        self.loan: List[Loan] = []
        self.list_adapter: List[ExternalDataBank] = []

    def searchUser(self, name: str, library):
        user = next((user for user in library.users if user.name == name), None)
        return user

    def foundBook(self, title: str, library):
        book = next((book for book in library.books if book.title == title), None)
        return book

    def searchLoan(self, idLoan: str, library):
        loan = next((loan for loan in library.loan if loan.idLoan == idLoan), None)
        return loan
    
    def addLoan(self, loan, library : 'Library'):
        library.loan.append(loan)

    def addBook(self, book: 'Book', library: 'Library'):
        library.books.append(book)
        # chama o notificador para alertar a adição de um novo livro para os usuários
        msg = BookAvailabilityNotifier()
        msg.notifyAddBook(book)
        
    def addUser(self, user, library: 'Library'):
        library.users.append(user)

################################################################
class ConfigurationManager:
        
    def catalog_books(self):
        #from models.book import Book
        book1 = Book("Harry Potter and the Philosopher's Stone", "J.K. Rowling", "BOTH", "Fantasy")
        book2 = Book("To Kill a Mockingbird", "Harper Lee", "BOTH",
                     "Classic Fiction")
        book3 = Book("1984", "George Orwell", "BOTH", "Dystopian")

        book4 = Book("Pride and Prejudice", "Jane Austen", "BOTH", "Romance")
        book5 = Book("The Great Gatsby", "F. Scott Fitzgerald", "BOTH", "Classic Fiction")
        book6 = Book("The Catcher in the Rye", "J.D. Salinger", "BOTH", "Coming-of-Age Fiction")
        book7 = Book("The Hobbit", "J.R.R. Tolkien", "BOTH", "Fantasy")
        book8 = Book("Moby Dick", "Herman Melville", "BOTH", "Adventure")
        book9 = Book("War and Peace", "Leo Tolstoy", "BOTH", "Historical Fiction")
        book10 = Book("The Alchemist", "Paulo Coelho", "BOTH", "Fiction")
        books = [book1, book2, book3, book4, book5, book6, book7, book8,book9, book10]
        
        return books
