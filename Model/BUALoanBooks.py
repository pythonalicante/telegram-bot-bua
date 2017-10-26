#!/usr/bin/env python
# -*- coding: utf-8 -*-


from Model import LoanBook


class BUALoanBooks:

    def __init__(self):
        self.clean()

    def clean(self):
        self.books = []

    def setBooks(self, dataBooks):
        for book in dataBooks:
            self.books.append(LoanBook(book))
