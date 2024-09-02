import uuid
from typing import List

from adapters.external_catalog_adapter import ExternalCatalogAdapter, ExternalDataBank
from models.book import Book
from models.library import Library


class User:
  name: str
  idUser: str
  email: str
  qntBooks: int

  def __init__(self, name, email, type):
    self.name = name
    self.idUser = str(uuid.uuid4())
    self.email = email
    self.qntBooks = 0
    self.type = type

  ##########################################################

  def searchBooks(self,adapter: 'ExternalCatalogAdapter',library: 'Library', busca: str):
    found_author = next(
        (book for book in library.books if book.author == busca), None)
    found_title = next(
        (book for book in library.books if book.title == busca), None)
    found_category = next(
        (book for book in library.books if book.category == busca), None)
    external_books= None
    #found_book= None
    if found_title:
        found_book = found_title
    elif found_author:
        found_book = found_author
    elif found_category:
        found_book = found_category
    else:
        external_books = adapter.searchDataBank(library, busca)

    if external_books:
      print('\nSeu livro foi encontrado no catálogo externo!')
      print(f"Titulo: {external_books.title}, Autor: {external_books.author}, Livro Disponível: {external_books.status}, Categoria: {external_books.category}\n")

    if 'found_book' in locals():
      # Tentando acessar a variável found_book
      print('\nSeu livro foi encontrado! Segue informações:')
      print(f"Titulo: {found_book.title}, Autor: {found_book.author}, Disponível: {found_book.status}, Categoria: {found_book.category}\n")
    elif not external_books: 
      print('Seu livro não foi encontrado :(\n')

  def addWaitingList(self, user: 'User', book: 'Book'):
    book.waitingList.append(user.idUser)
  
  def requestLoan(self, user, book):
    if not BookAvailabilityHandler().verifyStatus(book):
      user.addWaitingList(user, book)
      return False  #nao pode emprestar
    elif not UserEligibilityHandler().verifyAcess(user, book):
      return False  #nao pode emprestar
    else:
      return LoanLimitHandler().verifyLimit(user)  #aqui define se pode ou nao



#########################################################

class UserStudent(User):
  idStudent: str

  def __init__(self, name, email, type):
    super().__init__(name, email, type)
    #self.type = 'STUDENT'
    self.idStudent = str(uuid.uuid4())

##########################################################

class UserTeacher(User):
  idTeacher: str

  def __init__(self, name, email, type):
    super().__init__(name, email, type)
    #self.type = 'TEACHER'
    self.idTeacher = str(uuid.uuid4())

#####################################################

class UserEligibilityHandler:

  def verifyAcess(self, user: 'User', book: Book):
    if isinstance(user, UserStudent):
      user_type = 'STUDENT'
    elif isinstance(user, UserTeacher):
      user_type = 'TEACHER'
    else:
      user_type = 'NOTHING'

    #print(f'Confere UserEligibilityHandler: {book.acessBook} == {user_type}')
    #def verifyAcess(self, user: 'User', book: Book):
    return (book.acessBook == user_type or book.acessBook == 'BOTH')

########################################

class BookAvailabilityHandler:

  def verifyStatus(self, book: Book):  #vari retornar True(estatos disponivel)
    #print(f'\nConfere BookAvailabilityHandler: status ->{book.status}')
    return book.status

###########################################

class LoanLimitHandler:

  def verifyLimit(self, user: 'User'):
    user_type: str
    user_type = 'STUDENT' if isinstance(user, UserStudent) else 'TEACHER'
    if user_type == 'STUDENT':
      return user.qntBooks <= 4
    elif user_type == 'TEACHER':
      return user.qntBooks <= 5
