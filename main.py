import telebot
from telebot import types
import requests
import json
import random
from googletrans import Translator

TOKEN = '6317653802:AAHTP7Dv-4D-v0CIIinmdzq37I_CuGoj6_Q'
bot = telebot.TeleBot(TOKEN)
API = '3d33876b8a0d36c983f067a3c1e91c0a'
URL = 'https://api.telegram.org/bot'

keyboard = types.ReplyKeyboardMarkup(row_width=2)
translate_button = types.KeyboardButton('Переводчик')
weather_button = types.KeyboardButton('Погода')
calculator_button = types.KeyboardButton('Калькулятор')
mems_button = types.KeyboardButton('Мем дня')
info = types.KeyboardButton('Инфо')
keyboard.add(translate_button, weather_button, calculator_button, mems_button, info)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, чем могу помочь?', reply_markup=keyboard)
    bot.register_next_step_handler(message, on_click)


# Функция отображения кнопок
def buttons(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, "Выберите действие на панели команд", reply_markup=keyboard)


# Функция распознавания нажатия на кнопку и отправка в нужную функцию
@bot.message_handler(func=lambda m: True)
def on_click(message):
    if message.text == 'Переводчик':
        bot.send_message(message.chat.id, 'Введите слово для перевода:')
        bot.register_next_step_handler(message, translate)
    if message.text == 'Калькулятор':
        bot.send_message(message.chat.id, 'Введите выражение для вычисления:')
        bot.register_next_step_handler(message, calculator)
    if message.text == 'Погода':
        bot.send_message(message.chat.id, 'Введите город:')
        bot.register_next_step_handler(message, weather)
    if message.text == 'Мем дня':
        mem(message)
    if message.text == 'Инфо':
        info(message)


# Информация о разработчиках
def info(message):
    bot.send_message(message.chat.id,
                     'Разработчики:\n<b>Павлюченко Станислав Алексеевич и Ефимова Арина Владимировна</b>\n'
                     'Санкт-Петербург 2023 ',
                     parse_mode='HTML')


# Функция перевода текста
def translate(message):
    if message.text != '/translate':
        text_to_translate = message.text
        translator = Translator(service_urls=['translate.google.com'])
        translation = translator.translate(text_to_translate, src='en', dest='ru')
        bot.reply_to(message, translation.text)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите текст для перевода.')
    buttons(message)


# Функция калькулятор
def calculator(message):
    if message.text != '/calculator':
        expression = message.text
        try:
            result = eval(expression)
            bot.reply_to(message, f'Результат: {result}')
        except Exception as e:
            bot.send_message(message.chat.id, f'Произошла ошибка: {str(e)}')
    else:
        bot.send_message(message.chat.id, 'Введите выражение для вычисления:')
    buttons(message)


# Функция для определения погоды в выбранном вами городе
def weather(message):
    if message.text != '/weather':
        city = message.text.strip().lower()
        try:
            res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
            data = json.loads(res.text)
            city = data["name"]
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]

            bot.reply_to(message, f'Сейчас погода в городе: {city}\nТемпература: {temp}°C\n'
                                  f'Влажность: {humidity}%\nВетер: {wind} м/с')
        except:
            bot.send_message(message.chat.id, f'Произошла ошибка:\n Проверьте правильность написания города')
    else:
        bot.send_message(message.chat.id, 'Введите город:')
    buttons(message)


# Функция выдачи мема из паблика
def mem(message):
    public = random.randint(100, 300)
    chat_id = message.chat.id
    img_url = f'https://t.me/itmem_4U/{public}'
    request_url = f'{URL}{TOKEN}/sendPhoto?chat_id={chat_id}&photo={img_url}'
    response = requests.get(request_url)


bot.polling()