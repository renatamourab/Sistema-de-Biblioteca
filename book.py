import uuid
from typing import List

from models.category import BookCategory
from notifiers.book_availability_notifier import BookAvailabilityNotifier


class Book:
  title: str
  idBook: str
  author: str
  status: bool
  acessBook: str
  category: BookCategory

  def __init__(self, title, author, acessBook, category):
    self.title = title
    self.idBook = str(uuid.uuid4())
    self.author = author
    self.status = True
    self.acessBook = acessBook
    self.category = category
    self.waitingList: List[str] = []

  # atualiza status do livro
  def upStatusBook(self, book):
    self.status = not self.status  # True - disponível, False - indisponível
    if self.status:
      # chamando notificador para avisar quem estava na waiting list
      msg = BookAvailabilityNotifier()
      msg.notifyChangedStatus(book)
