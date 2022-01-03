import requests
import jsonpickle
import telebot
from telebot import types, custom_filters

import config

bot = telebot.TeleBot(config.TOKEN)

def get_token(login, psw):
    data = {
        'telephone_number': login,
        'password': psw,
    }
    post = requests.post(
        'https://api.snaptrap.online/api/user/login', json=data)
    token_tmp = jsonpickle.decode(post.text)['token']
    auth = {
        'Authorization': 'Bearer ' + token_tmp,
    }
    session = requests.get(
        'https://api.snaptrap.online/api/user/auth', headers=auth)
    token = jsonpickle.decode(session.text)['token']
    return token


class Product:
    files = 1
    name = 2
    price = 3
    type = 4


@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    """
    Start command. Here we are starting state
    """
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = 'media\\' + message.document.file_name
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
        if file_info.file_path.endswith('jpg') | file_info.file_path.endswith('png'):
            Product.files = {
                'img': open(src, 'rb')
            }
            Product.type = 'img'
        else:
            Product.files = {
                'img': open(src, 'rb')
            }
            Product.type = 'vid'

    bot.set_state(message.from_user.id, Product.name)
    bot.send_message(message.chat.id, 'Enter name')


@bot.message_handler(state=Product.name)
def name_get(message):
    """
    State 1. Will process when user's state is 1.
    """
    bot.send_message(message.chat.id, 'Price')
    bot.set_state(message.from_user.id, Product.price)
    with bot.retrieve_data(message.from_user.id) as data:
        data['name'] = message.text


# result
@bot.message_handler(state=Product.price, is_digit=True)
def ready_for_answer(message):
    with bot.retrieve_data(message.from_user.id) as data:
        bot.send_message(message.chat.id,
                         "Ready, take a look:\n<b>Name: {name}\nPrice: {price}\n</b>".format(
                             name=data['name'], price=message.text), parse_mode="html")
        data_post = {
            'name': data['name'],
            'price': message.text,
            'type': Product.type,
        }
        post = requests.post('https://api.snaptrap.online/api/goods/', data=data_post, files=Product.files, headers={
            'Authorization': 'Bearer ' + get_token('123456789', 'qwertyQW_1'),
        })
        bot.send_message(message.chat.id, 'Product added')
    bot.delete_state(message.from_user.id)


# incorrect number
@bot.message_handler(state=Product.price, is_digit=False)
def age_incorrect(message):
    bot.send_message(
        message.chat.id, 'Looks like you are submitting a string in the field age. Please enter a number')


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Registration")
    markup.add(item1)
    bot.send_message(message.chat.id, "Welcome" +
                     message.from_user.first_name, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def button_message(message):
    if message.text == "Registration":
        bot.send_message(message.from_user.id,
                         'https://snaptrap.online?tgID=' + str(message.chat.id))


# register filters

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())

# set saving states into file.
bot.enable_saving_states()  # you can delete this if you do not need to save states

bot.infinity_polling(skip_pending=True)
