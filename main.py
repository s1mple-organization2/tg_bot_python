import telebot
import requests
import jsonpickle
from telebot import types
from telebot import custom_filters

token = "5023550366:AAHHIsAIbrwI6S6ermjbeuZbvoa6Ye5qGwo"
bot = telebot.TeleBot(token)
token = {}


class Product:
    name = 'noname'
    price = 0
    type = 'none'
    files = {}


#
# def get_token(login, psw):
#     data = {
#         'telephone_number': login,
#         'password': psw,
#     }
#     post = requests.post('https://api.snaptrap.online/api/user/login', json=data)
#     token_tmp = jsonpickle.decode(post.text)['token']
#     auth = {
#         'Authorization': 'Bearer ' + token_tmp,
#     }
#     session = requests.get('https://api.snaptrap.online/api/user/auth', headers=auth)
#     token = jsonpickle.decode(session.text)['token']
#     return token
#
#
# @bot.message_handler(commands=['api'])
# def start_message(message):
#     response = requests.get('https://api.snaptrap.online/')
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     item1 = types.KeyboardButton("login")
#     item2 = types.KeyboardButton("all users")
#     markup.add(item1)
#     markup.add(item2)
#     bot.send_message(message.chat.id, response.text, reply_markup=markup)
#
#
# @bot.message_handler(commands=['get_id'])
# def button_message(message):
#     bot.send_message(message.chat.id, message.chat.id)
#
#
# @bot.message_handler(content_types=['text'])
# def button_message(message):
#     if message.text == "chat":
#         bot.send_message(5031837131, 'test_chat')
#
#
# @bot.message_handler(content_types='text')
# def message_reply(message):
#     if message.text == "login":
#         new = get_token('123456789', 'qwertyQW_1')
#         bot.send_message(message.chat.id, new)
#     elif message.text == "all users":
#         session = requests.get('http://localhost:8080/api/user/all', headers={
#             'Authorization': 'Bearer ' + get_token('123456789', 'qwertyQW_1'),
#         })
#         bot.send_message(message.chat.id, session.text)


# Загрузка товара(фото)
# @bot.message_handler(content_types=['document'])
# def handle_docs_photo(message):
#     file_info = bot.get_file(message.document.file_id)
#     downloaded_file = bot.download_file(file_info.file_path)
#     src = 'D:\projects\\tg_bot_snaptrap\media\\' + message.document.file_name
#
#     files = {
#         'img': open(src, 'rb')
#     }
#     bot.reply_to(message, "Enter product price")
#
#     @bot.message_handler(regexp=["\d"])
#
#     def message_product(message):
#         price = message.text
#         bot.reply_to(message, "Enter product name")
#
#         try:
#             chat_id = message.chat.id
#             file_info = bot.get_file(message.document.file_id)
#             downloaded_file = bot.download_file(file_info.file_path)
#             src = 'D:\projects\\tg_bot_snaptrap\media\\' + message.document.file_name
#             with open(src, 'wb') as new_file:
#                 new_file.write(downloaded_file)
#
#             data = {
#                 'name': 'test-8654352',
#                 'price': 434,
#                 'type': 'img',
#             }
#             files = {
#                 'img': open(src, 'rb')
#             }
#             post = requests.post('https://api.snaptrap.online/api/goods/', data=data, files=files, headers={
#                 'Authorization': 'Bearer ' + get_token('123456789', 'qwertyQW_1'),
#             })
#
#             bot.send_message(message.chat.id, post.text)
#
#             # bot.reply_to(message, "Пожалуй, я сохраню это")
#         except Exception as e:
#             bot.reply_to(message, e)

@bot.message_handler(commands=['test'])
def start_ex(message):
    """
    Start command. Here we are starting state
    """
    bot.set_state(message.from_user.id, Product.name)
    bot.send_message(message.chat.id, 'Product name')


@bot.message_handler(state="*", commands='cancel')
def any_state(message):
    """
    Cancel state
    """
    bot.send_message(message.chat.id, "Your state was cancelled.")
    bot.delete_state(message.from_user.id)


@bot.message_handler(state=Product.name)
def name_get(message):
    """
    State 1. Will process when user's state is 1.
    """
    bot.send_message(message.chat.id, f'Now write price')
    bot.set_state(message.from_user.id, Product.price)
    with bot.retrieve_data(message.from_user.id) as data:
        data['name'] = message.text


@bot.message_handler(state=Product.price)
def ask_age(message):
    """
    State 2. Will process when user's state is 2.
    """
    bot.send_message(message.chat.id, "write type")
    bot.set_state(message.from_user.id, Product.type)
    with bot.retrieve_data(message.from_user.id) as data:
        data['price'] = message.text


@bot.message_handler(state=Product.price, is_digit=True)
def ready_for_answer(message):
    with bot.retrieve_data(message.from_user.id) as data:
        bot.send_message(message.chat.id,
                         "Ready, take a look:\n<b>Name: {name}\n Price: {price}\n</b>".format(name=data['name'],
                                                                                              price=data['price']),
                         parse_mode="html")
    bot.delete_state(message.from_user.id)


bot.infinity_polling()
