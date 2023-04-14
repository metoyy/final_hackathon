import telebot
from telebot import types
from bs4 import BeautifulSoup as bs
import requests
import json
from decouple import config


token = config('TELEGRAM_TOKEN')
bot = telebot.TeleBot(token)

keyboard_start = types.ReplyKeyboardMarkup(resize_keyboard=True)

button_courseslist = types.KeyboardButton('Courses List')
button_consult = types.KeyboardButton('Заказать звонок')

keyboard_start.add(button_courseslist)
keyboard_start.add(button_consult)


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
    def send(self):
        request_call(self.number, self.question)

send_post = SendPost()

def parse_courses():
    soup = bs(requests.get('http://localhost:8000/api/parsing/courses/').text, 'lxml')
    text = soup.find('p').text
    ordered_dict = json.loads(text)
    returning_list = []
    for item in ordered_dict:
        returning_list.append(f'ID: {item["id"]}\nTitle: '
                              f'{item["title"]}\nCategory: {item["category"]}\n\
Duration: {item["duration_months"]} Months\nLanguage: {item["language"]}\n'
                              f'Price: {item["price"]} som')
    return returning_list


def request_call(number, question):
    requests.post('http://localhost:8000/api/parsing/calls/',
                  data=[('number', number), ('question', question)])
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
    else:
        answer = bot.send_message(message.chat.id, 'what?', reply_markup=keyboard_start)
        bot.register_next_step_handler(answer, handle_answer)


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
    send_post.send()
    ans = bot.send_message(message.chat.id, 'Done! Request to call sent! '
                                      'Choose what you want?', reply_markup=keyboard_start)
    bot.register_next_step_handler(ans, handle_answer)


bot.polling()
