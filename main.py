import telebot
from telebot import types



TOKEN = '6317653802:AAHTP7Dv-4D-v0CIIinmdzq37I_CuGoj6_Q'
bot = telebot.TeleBot(TOKEN)


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



# Функция отображения кнопок
def buttons(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, "Выберите действие на панели команд", reply_markup=keyboard)




# Информация о разработчиках
def info(message):
    bot.send_message(message.chat.id,
                     'Разработчики:\n<b>Павлюченко Станислав Алексеевич и Ефимова Арина Владимировна</b>\n'
                     'Санкт-Петербург 2023 ',
                     parse_mode='HTML')











bot.polling()
