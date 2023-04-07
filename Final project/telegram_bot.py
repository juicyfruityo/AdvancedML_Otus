import numpy as np
import pickle
from rapidfuzz import process

import telebot
from telebot import types


with open('result/authors_dict_v1.pkl', 'rb') as file:
    authors_dict = pickle.load(file)

with open('result/books_dict_v1.pkl', 'rb') as file:
    books_dict = pickle.load(file)

authors_dict = {key.lower(): [name.lower() for name in value] for key, value in authors_dict.items()}
books_dict = {key.lower(): [name.lower() for name in value] for key, value in books_dict.items()}

books_names = list(books_dict.keys())
authors_names = list(authors_dict.keys())


TOKEN = '5729687819:AAFNazpsKPppMG8J73rb5Iu_jFakAxoMd5s'

bot = telebot.TeleBot(TOKEN)


markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn_books = types.InlineKeyboardButton('/similar_books')
btn_authors = types.InlineKeyboardButton('/similar_authors')
markup.add(btn_books, btn_authors)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id, 
        '''
Привет! ✌️
Здесь можно подобрать книги или авторов, похожих на прочитанных и интересных тебе.
Название книг и имена авторов следует писать на английском.
Выбирай одну из двух команд.
        ''',
        reply_markup=markup
        )


@bot.message_handler(commands=['similar_books'])
def find_similar_books(message):
    bot.send_message(
        message.chat.id, 
        "Введи название книги (на англ.):",
        reply_markup=markup
        )
    bot.register_next_step_handler(
        message, fetch_similar_books)

def fetch_similar_books(message):
    if books_dict.get(message.text.lower()) is not None:
        book_names = books_dict[message.text.lower()]
        reply = "\n".join(book_names)

        bot.send_message(
            message.chat.id, 
            reply,
            reply_markup=markup
            )

    else:
        reply = f"Такой книги не нашлось: {message.text}\n Может быть имелось ввиду одно из названий:"
        bot.send_message(
            message.chat.id, 
            reply,
            reply_markup=markup
            )

        similar_names = process.extract(message.text.lower(), books_names, limit=5)
        reply = "\n".join([name[0] for name in similar_names])
        bot.send_message(
            message.chat.id, 
            reply,
            reply_markup=markup
            )

    


@bot.message_handler(commands=['similar_authors'])
def find_similar_authors(message):
    bot.send_message(
        message.chat.id, 
        "Введи имя автора (на англ.):",
        reply_markup=markup
        )
    bot.register_next_step_handler(
    message, fetch_similar_authors)

def fetch_similar_authors(message):
    if authors_dict.get(message.text.lower()) is not None:
        author_names = authors_dict[message.text.lower()]
        reply = "\n".join(author_names)

        bot.send_message(
            message.chat.id, 
            reply,
            reply_markup=markup
            )

    else:
        reply = f"Такого автора не нашлось: {message.text}\n Может быть имелось ввиду одно из имён:"
        bot.send_message(
            message.chat.id, 
            reply,
            reply_markup=markup
            )

        similar_names = process.extract(message.text.lower(), authors_names, limit=5)
        reply = "\n".join([name[0] for name in similar_names])
        bot.send_message(
            message.chat.id, 
            reply,
            reply_markup=markup
            )



bot.infinity_polling()