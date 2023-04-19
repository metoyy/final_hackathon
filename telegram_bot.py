import telebot
from telebot import types
from bs4 import BeautifulSoup as bs
import requests
import json
from decouple import config

token = config('TELEGRAM_TOKEN')
bot = telebot.TeleBot(token)

keyboard_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_usermenu = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_usermenu_anon = types.ReplyKeyboardMarkup(resize_keyboard=True)

button_courseslist = types.KeyboardButton('Courses List')
button_consult = types.KeyboardButton('Заказать звонок')
button_usermenu = types.KeyboardButton('Меню пользователя')
button_linkacc = types.KeyboardButton('Link account')
button_details = types.KeyboardButton('Account details')
button_update_det = types.KeyboardButton('Update details')
button_unlink = types.KeyboardButton('Unlink account')
button_mainmenu = types.KeyboardButton('Main menu')

keyboard_start.add(button_courseslist)
keyboard_start.add(button_consult)
keyboard_start.add(button_usermenu)

keyboard_usermenu.add(button_details)
keyboard_usermenu.add(button_update_det)
keyboard_usermenu.add(button_unlink)
keyboard_usermenu.add(button_mainmenu)

keyboard_usermenu_anon.add(button_linkacc)

class Info:
    def __init__(self, eur):
        self.anon = eur


class SendPost:
    def add(self, **kwargs):
        try:
            self.number = kwargs.pop('number')
        except:
            pass
        try:
            self.question = kwargs.pop('question')
        except:
            pass
        try: 
            self.account = kwargs.pop('account')
        except:
            pass
    def send(self):
        request_call(self.number, self.question, self.account)


class SendEmailInfo:
    def add(self, **kwargs):
        try:
            self.email = kwargs.pop('email')
        except:
            pass
        try:
            self.username = kwargs.pop('username')
        except:
            pass




send_post = SendPost()

def parse_courses():
    soup = bs(requests.get('http://34.90.36.69/api/parsing/courses/').text, 'lxml')
    text = soup.find('p').text
    ordered_dict = json.loads(text)
    returning_list = []
    for item in ordered_dict:
        returning_list.append(f'ID: {item["id"]}\nTitle: '
                              f'{item["title"]}\nCategory: {item["category"]}\n\
Duration: {item["duration_months"]} Months\nLanguage: {item["language"]}\n'
                              f'Price: {item["price"]} som')
    return returning_list


def request_call(number, question, username):
    requests.post('http://34.90.36.69/api/parsing/calls/',
                  data=[('number', number), ('question', question), ('telegram_user', username)])
    return 0


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Hello this is Hackathon Unify project \
                     parser')
    answer = bot.send_message(message.chat.id, 'Choose what you want?', reply_markup=keyboard_start)
    bot.register_next_step_handler(answer, handle_answer)


@bot.message_handler(commands=['stop'])
def stop_message(message):
    bot.send_message(message.chat.id, 'Goodbye!')


def handle_answer(message):
    if message.text.lower() == 'courses list':
        users_list(message)
    elif message.text.lower() == 'заказать звонок':
        gain_info(message)
    elif message.text.lower() == 'меню пользователя':
        user_menu(message)
    else:
        answer = bot.send_message(message.chat.id, 'what?', reply_markup=keyboard_start)
        bot.register_next_step_handler(answer, handle_answer)


def handle_usermenu(message):
    if message.text.lower() == 'link account':
        clarify_info1(message)
    elif message.text.lower() == 'main menu':
        start_message(message)
    else:
        answer = bot.send_message(message.chat.id, 'what?')
        bot.register_next_step_handler(answer, handle_usermenu)


def gain_info(message):
    number = bot.send_message(message.chat.id, 'Enter your number...')
    bot.register_next_step_handler(number, posts_list)


def users_list(message):
    result = parse_courses()
    if not result:
        bot.send_message(message.chat.id, 'No courses available')
    for item in result:
        bot.send_message(message.chat.id, item)
    answer = bot.send_message(message.chat.id, 'Choose what you want?', reply_markup=keyboard_start)
    bot.register_next_step_handler(answer, handle_answer)


def posts_list(message):
    global send_post
    send_post.add(number=message.text)
    question = bot.send_message(message.chat.id, 'Enter your question... ')
    bot.register_next_step_handler(question, final_bro)


def final_bro(message):
    global send_post
    send_post.add(question=message.text)
    send_post.add(account=message.chat.username)
    send_post.send()
    ans = bot.send_message(message.chat.id, 'Done! Request to call sent! '
                                      'Choose what you want?', reply_markup=keyboard_start)
    bot.register_next_step_handler(ans, handle_answer)


def user_menu(message):
    ans = bot.send_message(message.chat.id, "What do you want?", reply_markup=keyboard_usermenu_anon)
    bot.register_next_step_handler(ans, user_menu,)


def clarify_info1(message):
    ans = bot.send_message(message.chat.id, 'Write your email...')
    bot.register_next_step_handler(ans, clarify_info2)


def clarify_info2(message):
    email = message.text
    User = SendEmailInfo()
    User.add(email=email, username=message.chat.username)
    response = requests.patch('http://34.90.36.69/api/parsing/addaccount/', data=[('email', User.email),
                                                                                  ('username', User.username)])
    print(response)

    # ans = bot.send_message(message.chat.id, )






bot.polling()
