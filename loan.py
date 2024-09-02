import uuid
from datetime import datetime, timedelta

from models.book import Book

#from models.library import Library
from models.user import User


class Loan:
  idLoan: str  #USUARIO VAI TER ACESSO AO IDlOAN PARA DEVOLVER
  book: Book
  user: User
  loanDate: datetime
  endDate: datetime

  #  finalDate: datetime

  #aqui apos aprovação damos um doLoan, que cria o emprestimo
  def __init__(self, book, user):
    self.idLoan = str(uuid.uuid4())
    self.book = book
    self.user = user
    self.loanDate = datetime.now()
    self.endDate = datetime.now() + timedelta(days=7)  #1 semana para devolver
    book.upStatusBook(book)  #muda status pra False
    user.qntBooks += 1  #adiciona o livro na qtd de empretimos

  #adiciona a loan na library
  

  #remove a loan
  def returnLoan(self, user, book):  #rever
    user.qntBooks -= 1
    book.upStatusBook(book)