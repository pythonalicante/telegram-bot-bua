#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO: Improve the next two lines

from BUACrawler import BUACrawler
from BUALoanBooks import BUALoanBooks
from BUACatalog import BUACatalog
from LoginException import InvalidCredentialsException, UnloggedUserException, AlreadyLoggedUserException
from CatalogException import NoSearchException, OnlyOnePageException, BookIndexOutbound


class BUA:

    def __init__(self):
        self.__crawler = BUACrawler()
        self.__catalog = BUACatalog()
        self.__loansBooks = BUALoanBooks()
        self.__userId = ''

        self.__isOnCatalog = False
        self.__isLogged = False
        self.__isRenovatingBooks = False

    def login(self, user, secret):
        if not self.__isLogged:
            self.__isLogged = self.__crawler.login(user, secret)
            if not self.__isLogged:
                raise InvalidCredentialsException()
            self.__userId = user
        else:
            raise AlreadyLoggedUserException()

    def disconnect(self):
        if not self.__isLogged:
            raise UnloggedUserException()

        self.__crawler.disconnect()
        self.__isLogged = True
        self.__isOnCatalog = False
        self.__isRenovatingBooks = False

    def showLoans(self):
        self.__isOnCatalog = False
        self.__catalog.clean()
        self.__loansBooks.clean()
        if not self.__isLogged:
            raise UnloggedUserException()

        self.__isRenovatingBooks = True
        self.__loansBooks.setBooks(self.__crawler.showLoans())
        return self.__loansBooks.books

    def loanAllBooks(self):

        if not self.__isLogged:
            raise UnloggedUserException()

        self.__crawler.loanAllBooks(self.__userId)
        return self.showLoans()

    def searchBook(self, name):
        self.__catalog.clean()
        self.__loansBooks.clean()
        self.__isRenovatingBooks = False
        dataForBookSearched = self.__crawler.searchBook(name)
        self.__catalog.setBooks(dataForBookSearched[0])
        self.__catalog.page = 1
        self.__catalog.numPages = dataForBookSearched[1]
        self.__catalog.pageIndexs = dataForBookSearched[2]
        self.__isOnCatalog = True
        return self.__catalog.books

    def stepBackward(self):
        self.__crawler.stepBackward()

    def localizationsForBook(self, idBook):
        if not self.__isOnCatalog:
            raise NoSearchException()

        if idBook < 0 or idBook >= len(self.__catalog.books):
            raise BookIndexOutbound()

        viewId = self.__catalog.books[idBook].viewAction
        locations = self.__crawler.localizationsForBook(
            viewId, self.__catalog.page)
        self.stepBackward()
        return locations

    def nextPage(self):
        if not self.__isOnCatalog:
            raise NoSearchException()

        if self.__catalog.numPages == 1:
            raise OnlyOnePageException()

        if self.__catalog.page < self.__catalog.numPages:
            self.__catalog.page += 1
            self.__catalog.setBooks(
                self.__crawler.nextPageOf__catalog(self.__catalog.pageIndexs))

        return self.__catalog.books

    def lastPage(self):

        if not self.__isOnCatalog:
            raise NoSearchException()

        if self.__catalog.numPages == 1:
            raise OnlyOnePageException()

        if self.__catalog.page > 1:
            self.__catalog.page -= 1
            self.__catalog.setBooks(
                self.__crawler.nextPageOf__catalog(self.__catalog.pageIndexs))
        return self.__catalog.books
