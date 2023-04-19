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
button_consult = types.KeyboardButton('Leave a call')
button_usermenu = types.KeyboardButton('User menu')
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
keyboard_usermenu_anon.add(button_mainmenu)

keyboard_update_choose = types.ReplyKeyboardMarkup(resize_keyboard=True)

button_firstname = types.KeyboardButton('First name')
button_lastname = types.KeyboardButton('Last name')
button_username = types.KeyboardButton('Username')

keyboard_update_choose.add(button_firstname)
keyboard_update_choose.add(button_lastname)
keyboard_update_choose.add(button_username)


class Info:
    def __init__(self, eur):
        self.anon = eur


USER_FIELDS = (
    "id",
    "last_login",
    "is_superuser",
    "is_staff",
    "date_joined",
    "email",
    "activation_code",
    "username",
    "first_name",
    "last_name",
    "telegram_username",
    "tg_code",
    "is_active",
    "groups",
    "user_permissions",
)

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


def what_menu(username):
    response = requests.get('http://34.90.36.69/api/parsing/checkview/', data=[('username', username)])
    if response.status_code == 400:
        return handle_usermenu
    else:
        return handle_usermenu_auth


def is_linked(username):
    response = requests.get('http://34.90.36.69/api/parsing/checkview/', data=[('username', username)])
    if response.status_code == 400:
        return keyboard_usermenu_anon
    else:
        return keyboard_usermenu


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
    elif message.text.lower() == 'leave a call':
        gain_info(message)
    elif message.text.lower() == 'user menu':
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
        answer = bot.send_message(message.chat.id, 'what?', reply_markup=is_linked(message.chat.username))
        bot.register_next_step_handler(answer, handle_usermenu)


def handle_usermenu_auth(message):
    if message.text.lower() == 'account details':
        account_details(message)
    elif message.text.lower() == 'update details':
        account_update(message)
    elif message.text.lower() == 'unlink account':
        account_unlink(message)
    elif message.text.lower() == 'main menu':
        start_message(message)
    else:
        answer = bot.send_message(message.chat.id, 'what?', reply_markup=is_linked(message.chat.username))
        bot.register_next_step_handler(answer, handle_usermenu_auth)


def choose_update(message):
    tex = message.text.lower()
    if tex == 'first name':
        msg = bot.send_message(message.chat.id, 'Send new first name...')
        bot.register_next_step_handler(msg, update_firstname)
    elif tex == 'last name':
        msg = bot.send_message(message.chat.id, 'Send new last name...')
        bot.register_next_step_handler(msg, update_lastname)
    elif tex == 'username':
        msg = bot.send_message(message.chat.id, 'Send new username...')
        bot.register_next_step_handler(msg, update_username)
    elif tex == 'main menu':
        handle_usermenu_auth(message)
    else:
        ans = bot.send_message(message.chat.id, 'What?')
        bot.register_next_step_handler(ans, choose_update)


def update_username(message):
    response = requests.patch(f'http://34.90.36.69/api/parsing/accountdetails/{message.chat.username}/',
                              data=[('username', message.text)])
    ans = bot.send_message(message.chat.id, response.text, reply_markup=is_linked(message.chat.username))
    bot.register_next_step_handler(ans, what_menu(message.chat.username))


def update_firstname(message):
    response = requests.patch(f'http://34.90.36.69/api/parsing/accountdetails/{message.chat.username}/',
                              data=[('first_name', message.text)])
    ans = bot.send_message(message.chat.id, response.text, reply_markup=is_linked(message.chat.username))
    bot.register_next_step_handler(ans, what_menu(message.chat.username))


def update_lastname(message):
    response = requests.patch(f'http://34.90.36.69/api/parsing/accountdetails/{message.chat.username}/',
                              data=[('last_name', message.text)])
    ans = bot.send_message(message.chat.id, response.text, reply_markup=is_linked(message.chat.username))
    bot.register_next_step_handler(ans, what_menu(message.chat.username))


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
    ans = bot.send_message(message.chat.id, "What do you want?", reply_markup=is_linked(message.chat.username))
    bot.register_next_step_handler(ans, what_menu(message.chat.username))


def clarify_info1(message):
    response = requests.get('http://34.90.36.69/api/parsing/checkview/', data=[('username', message.chat.username)])
    print(response.status_code, '\n\n', response.text)
    if response.status_code == 200:
        ans = bot.send_message(message.chat.id, 'You already linked your account! Unlink first!',
                               reply_markup=keyboard_usermenu)
        bot.register_next_step_handler(ans, handle_usermenu)
    elif response.status_code == 400:
        ans = bot.send_message(message.chat.id, 'Write your email...')
        bot.register_next_step_handler(ans, clarify_info2)
    else:
        ans = bot.send_message(message.chat.id, 'Error!', reply_markup=is_linked(message.chat.username))
        bot.register_next_step_handler(ans, what_menu(message.chat.username))


def clarify_info2(message):
    email = message.text
    User = SendEmailInfo()
    User.add(email=email, username=message.chat.username)
    response = requests.patch('http://34.90.36.69/api/parsing/addaccount/', data=[('email', User.email),
                                                                                  ('username', User.username)])
    msg = ('Message to your email successfully sent. Check your inbox and write the code here...',
           link_accounts, None) if not response.status_code == 404\
        else (f'Error! {json.loads(response.text)["msg"]}\n\nWent back to the main users menu',
              what_menu(message.chat.username),
              is_linked(message.chat.username))
    ans = bot.send_message(message.chat.id, msg[0], reply_markup=msg[2])
    bot.register_next_step_handler(ans, msg[1])


def link_accounts(message):
    code = message.text
    username = message.chat.username
    response = requests.post('http://34.90.36.69/api/parsing/addaccount/', data=[('code', code),
                                                                                 ('username', username)])
    respon = json.loads(response.text)
    ans = bot.send_message(message.chat.id, respon['msg'], reply_markup=keyboard_usermenu)
    bot.register_next_step_handler(ans, what_menu(username))


def account_details(message):
    response = requests.get(f'http://34.90.36.69/api/parsing/accountdetails/{message.chat.username}/')
    json_ = json.loads(response.text)
    text = f'First name: {json_.get("first_name")}\nLast name: {json_.get("last_name")}\n' \
           f'Date joined: {json_.get("date_joined")}\nEmail: {json_.get("email")}\nUsername: {json_.get("username")}'
    ans = bot.send_message(message.chat.id, text, reply_markup=keyboard_usermenu)
    bot.register_next_step_handler(ans, handle_usermenu_auth)


def account_update(message):
    ans = bot.send_message(message.chat.id, 'Choose what you want to update...', reply_markup=keyboard_update_choose)
    bot.register_next_step_handler(ans, choose_update)


def account_unlink(message):
    response = requests.delete('http://34.90.36.69/api/parsing/addaccount/',
                               data=[('username', message.chat.username)])
    msg = response.text
    print(msg)
    ans = bot.send_message(message.chat.id, 'msg', reply_markup=is_linked(message.chat.username))
    bot.register_next_step_handler(ans, what_menu(message.chat.username))


bot.polling()
