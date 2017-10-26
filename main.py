# !/usr/bin/python
# -*- coding: utf-8 -*-

import telegram.ext
from Bot import BUABot
bua = BUABot.BUABot()

# bot's token
TOKEN = ':-'

#@verdej0
# all the functions must return a string with success, error or the info


def login(bot, update, args):
    text = ''
    if(len(args) == 2):
        text += bua.login(args[0], args[1])
        update.message.reply_text(text)
    else:
        update.message.reply_text(
            "Error en los parametros.\nUso /login user password")


def disconnect(bot, update):
    text = ''
    text = bua.disconnect()
    update.message.reply_text(text)

# Search books, and search for a book location


def catalog(bot, update, args):
    text = ''
    USAGE = 'Error en los argumentos.\n Uso:\n /catalog search bookname\n /catalog nextPage\n/catalog lastPage\n/catalog location bookid'
    if(len(args) == 1):
        if(str.lower(args[0]) == 'nextpage'):
            text = bua.nextPage()
        elif(str.lower(args[0]) == 'lastpage'):
            text = bua.lastPage()
        else:
            text = USAGE

    elif(len(args) == 2):
        if(str.lower(args[0]) == 'search'):
            text = bua.searchBook(args[1])
        elif(str.lower(args[0]) == 'location'):
            text = bua.localizationForBook(args[1])
        else:
            text = USAGE
    else:
        text = USAGE

    update.message.reply_text(text)


# View the loans
def myBooks(bot, update):
    text = ''
    text = bua.showLoans()
    update.message.reply_text(text)

# Renew all the loans


def loanBooks(bot, update):
    text = ''
    text = bua.loanAllBooks()
    update.message.reply_text(text)


def help(bot, update):
    update.message.reply_text('Help:\n/login - Loggearte en la Bua.\n/logout - Cerrar sesion.\n/catalog search _bookname_.\n/catalog location _bookId_.\n/catalog nextPage.\n/catalog lastPage.\n/myBooks - Lista tus libros prestados.\n/loanBooks - Renueva todos tus libros\n/myBooks - Lista tus libros prestados.\n/loanBooks - Renueva todos tus libros..')


def start(bot, update):
    name = update.message.from_user.name
    update.message.reply_text(
        'Hola ' + name + ', pulsa /help para saber qué hago')


def main():

    updater = telegram.ext.Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(telegram.ext.CommandHandler("login", login, pass_args=True))
    dp.add_handler(telegram.ext.CommandHandler("logout", disconnect))
    dp.add_handler(telegram.ext.CommandHandler(
        "catalog", catalog, pass_args=True))
    dp.add_handler(telegram.ext.CommandHandler("mybooks", myBooks))
    dp.add_handler(telegram.ext.CommandHandler("loanbooks", loanBooks))
    dp.add_handler(telegram.ext.CommandHandler("help", help))
    dp.add_handler(telegram.ext.CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
