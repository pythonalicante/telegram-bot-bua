#!/usr/bin/env python
# coding: utf-8


class CatalogBook:

    def __init__(self, data):
        self.viewAction = ''
        self.title = ''
        self.author = ''

        if len(data) > 0:
            dataStr = str(data[0])
            self.viewAction = dataStr[0:4] + '^' + dataStr[4:len(dataStr)]
        if len(data) > 1:
            self.title = data[1]
        if len(data) > 2:
            self.author = data[2]

    def __toString(self):
        info = ''
        if not self.title == '':
            info += self.title
        if not self.author == '':
            info += ' | ' + self.author
        return info

    def __str__(self):
        return self.__toString()

    # ##DOC: Python2 and Python3 compatibility
    def __repr__(self):
        return self.__toString()
