from abc import ABC, abstractmethod

from adapters.external_catalog_adapter import ExternalCatalogAdapter
from models.book import Book
from models.library import Library
from models.loan import Loan
from models.user import User, UserStudent, UserTeacher


class Mediator(ABC):

  @abstractmethod
  def searchBooks(self, data, library):
    pass

  @abstractmethod
  def lendBook(self, user, book, library):
    pass

  @abstractmethod
  def returnBook(self, loan, library):
    pass

  @abstractmethod
  def createBook(self, data, library):
    pass

  @abstractmethod
  def createUser(self, data, library):
    pass
    
  @abstractmethod
  def searchUser(self, data, library):
    pass

  @abstractmethod
  def foundBook(self, data, library):
    pass

####################################################################

class LibraryMediator(Mediator):
  
  def __init__(self):
    library = Library()
    #self.adapter = ExternalCatalogAdapter()
    #self.library = library

  def searchBooks(self, data, library):
    #data = [user, livro_busca, adapter]
    user= data[0]
    busca=data[1]        # lista de adapters
    adapter=data[2]        #classe adapter
    user.searchBooks(adapter, library, busca)

  def lendBook(self, user: 'User', book: 'Book', library: 'Library'):
    #aqui agrupamos alguns metodos
    #vemos se o usuario pode fazer o emprestimo
    # se pode, fazemos e adicionamos a lista de loans
    if user.requestLoan(user, book):
      new_loan = Loan(book, user)
      library.addLoan(new_loan, library)
      print(f'Seu empréstimo foi realizado! Você tem até dia {new_loan.endDate} para devolver.\n')
      print(f' Ah, se codigo de emprestimo é {new_loan.idLoan}, lembre-se de anota-lo para a devolução do livro. Aproveite a leitura :)\n')
    else:
      print('Seu empréstimo não foi aprovado :(\n') #n foi aprovado,e vai lista de espera

  def returnBook(self, loan: 'Loan', library): 
    #aqui a gente vai perguntar o id do livro que o usuario quer devolver
    loan.returnLoan(loan.user, loan.book)
    print('Livro devolvido com sucesso!\n')
  
  def createBook(self, data, library):
    title=data[0]
    author=data[1]
    category=data[2]
    acessBook = data [3]
    book=Book(title, author, category, acessBook)
    library.addBook(book, library)

  def createUser(self, data, library):
    if data[2] == 'STUDENT':
      user=UserStudent(data[0], data[1], data[2])
    else:
      user=UserTeacher(data[0], data[1], data[2])
    library.addUser(user, library)
    print(f'{user.name}, seja bem vindo a nossa biblioteca!\n')

  def searchUser(self, data, library):
    user= library.searchUser(data, library)
    return user

  def searchLoan(self, data, library):
    loan= library.searchLoan(data, library)
    return loan

  def foundBook(self, data, library):
    book= library.foundBook(data, library)
    return book