#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
import Utils
from bs4 import BeautifulSoup as bs

header = {'content-type': 'application/x-www-form-urlencoded'}
nameSearchForm = 'searchform'
nameNewSessionForm = 'loginform'
nameHitlistForm = 'hitlist'
nameRenewBooksForm = 'renewitems'
urlBase = 'http://gaudi.ua.es'
firstAction = '/uhtbin/cgisirsi/x/x/0/49/'


class BUACrawler:

    def __init__(self):
        self.__currentUrl = urlBase + firstAction
        self.__currentPage = requests.get(self.__currentUrl).content
        self.__urlScrapped = None

    def __getActionOfForm(self, formName):
        self.__urlScrapped = bs(self.__currentPage, 'html.parser')
        forms = self.__urlScrapped.find_all('form')
        action = ''
        for form in forms:
            if form.attrs.get('name') == formName:
                action = form.attrs.get('action')
                break
        return action

    def __catalogLastPageIndex(self):
        self.__urlScrapped = bs(self.__currentPage, 'html.parser')
        setOfP = self.__urlScrapped.find_all('p', {'class': 'searchsum'})
        bookSearchPages = []
        for p in setOfP:
            if 'href' in str(p):
                pages = p.find_all('a')
                if len(pages) == 3:
                    bookSearchPages = [1, 20]
                else:
                    last = (len(pages) - 2) * 20
                    bookSearchPages = [last - 19, last]
                break

        return bookSearchPages

    def __extractBooksOfCurrentPage(self):
        self.__urlScrapped = bs(self.__currentPage, 'html.parser')
        setOfTables = self.__urlScrapped.find_all('td', {'class': 'searchsum'})

        books = []

        if len(setOfTables) == 0:
            return books

        items = setOfTables[0].find_all('table')

        for i in range(1, len(items) - 1):
            label = items[i].find_all('td')[4].find_all('label')
            matches = re.finditer(Utils.catalogBookRegex, str(label))
            for match in matches:
                books.append(match.groups())

        return books

    def stepBackward(self):
        self.__urlScrapped = bs(self.__currentPage, 'html.parser')
        tables = self.__urlScrapped.find('table', {'class', 'gatewaystyle'})
        action = tables.find('tr').find('td').find_all('a')[
            0].attrs.get('href')
        self.__currentUrl = urlBase + action
        self.__currentPage = requests.get(self.__currentUrl).content

    def searchBook(self, bookName):

        # Go to catalog menu section
        books = []
        self.__urlScrapped = bs(self.__currentPage, 'html.parser')
        setOfTd = self.__urlScrapped.find_all('td', {'class': 'rootbarcell'})
        action = ''
        for td in setOfTd:
            if 'href' in str(td):
                action = td.find_all('a')[0].attrs.get('href')
                break

        if action == '':
            return books

        self.__currentUrl = urlBase + action
        self.__currentPage = requests.get(self.__currentUrl).content

        action = self.__getActionOfForm(nameSearchForm)
        self.__currentUrl = urlBase + action
        payload = {
            'query_type': 'search',
            'searchdata1': bookName,
            'srchfield1': 'GENERAL^SUBJECT^GENERAL^^Todos los campos',
            'library': '',
            'sort_by': 'TI',
        }
        response = requests.post(
            self.__currentUrl, data=payload, headers=header)
        self.__currentPage = response.content
        pagesIndex = self.__catalogLastPageIndex()
        books = self.__extractBooksOfCurrentPage()
        numPages = 1
        if len(pagesIndex) == 2:
            numPages = pagesIndex[1] / 20 + 1
        return [books, numPages, pagesIndex]

    def localizationsForBook(self, viewName, currentPage):

        locations = []
        last_hit = currentPage * 20
        first_hit = last_hit - 19

        action = self.__getActionOfForm(nameHitlistForm)
        self.__currentUrl = urlBase + action
        payload = {'first_hit': first_hit,
                   'last_hit': last_hit,
                   'form_type': '',
                   viewName: 'Detalles'}

        response = requests.post(
            self.__currentUrl, data=payload, headers=header)
        self.__currentPage = response.content
        self.__urlScrapped = bs(self.__currentPage, 'html.parser')

        panel1 = self.__urlScrapped.find('div', {'id': 'panel1'})

        tables = panel1.find_all('table')
        if len(tables) < 2:
            return locations

        trSet = tables[1].find_all('tr')
        if len(tables) == 0:
            return locations

        for index in range(2, len(trSet)):
            tdSet = trSet[index].find_all('td')

            signature = ''
            location = ''
            if len(tdSet) > 1:
                signature = tdSet[0].next.lstrip()
            if len(tdSet) == 4:
                location = tdSet[3].next.lstrip()

            if signature == '' and len(locations) > 0:
                signature = locations[len(locations) - 1][0]
            locations.append([signature, location])

        return locations

    def nextPageOfCatalog(self, indexPagination):
        action = self.__getActionOfForm(nameHitlistForm)
        self.__currentUrl = urlBase + action
        payload = {'first_hit': indexPagination[0],
                   'last_hit': indexPagination[1],
                   'form_type': 'SCROLL^F'}
        response = requests.post(self.__currentUrl, data=payload,
                                 headers=header)
        self.__currentPage = response.content
        return self.__extractBooksOfCurrentPage()

    def lastPageOfCatalog(self, indexPagination):
        action = self.__getActionOfForm(nameHitlistForm)
        self.__currentUrl = urlBase + action
        payload = {'first_hit': indexPagination[0],
                   'last_hit': indexPagination[1],
                   'form_type': 'SCROLL^B'}
        response = requests.post(self.__currentUrl, data=payload,
                                 headers=header)
        self.__currentPage = response.content
        return self.__extractBooksOfCurrentPage()

    def showLoans(self):

        # This enters in link 'Servios al usuario'
        books = []
        self.__urlScrapped = bs(self.__currentPage, 'html.parser')
        setOfTd = self.__urlScrapped.find_all('td', {'class': 'rootbarcell'})
        action = ''
        for td in setOfTd:
            if 'href' in str(td):
                action = td.find_all('a')[-2].attrs.get('href')
                break

        if action == '':
            return books

        self.__currentUrl = urlBase + action
        self.__currentPage = requests.get(self.__currentUrl).content

        # This enters in link 'Renovar Prestamos'
        self.__urlScrapped = bs(self.__currentPage, 'html.parser')
        tables = self.__urlScrapped.find_all('table',
                                             {'class': 'defaultstyle'})
        action = tables[0].find_all('a')[-1].attrs.get('href')

        if action == '':
            return books

        self.__currentUrl = urlBase + action
        self.__currentPage = requests.get(self.__currentUrl).content
        matches = re.finditer(Utils.loanBooksRegex, self.__currentPage)
        for match in matches:
            books.append(match.groups())

        return books

    def loanAllBooks(self, userId):
        action = self.__getActionOfForm(nameRenewBooksForm)
        self.__currentUrl = urlBase + action
        payload = {'user_id': userId, 'selection_type': 'all'}
        self.__currentPage = requests.post(
            self.__currentUrl, data=payload, headers=header).content

    def login(self, user, secret):
        action = self.__getActionOfForm(nameNewSessionForm)
        self.__currentUrl = urlBase + action
        payload = {'user_id': user, 'password': secret}
        response = requests.post(
            self.__currentUrl, data=payload, headers=header)
        self.__currentPage = response.content

        self.__urlScrapped = bs(self.__currentPage, 'html.parser')
        if self.__urlScrapped.find('div', {'class': 'pagecontainer3pg'}) == None:
            return False
        return True

    def disconnect(self):
        self.__urlScrapped = bs(self.__currentPage, 'html.parser')
        tables = self.__urlScrapped.find_all(
            'table', {'class': 'gatewaystyle'})
        action = tables[0].find_all('a')[-1].attrs.get('href')
        self.__currentUrl = urlBase + action
        self.__currentPage = requests.post(self.__currentUrl).content
        self.__urlScrapped = None
        self.__currentUrl = urlBase + firstAction
        self.__currentPage = requests.get(self.__currentUrl).content
