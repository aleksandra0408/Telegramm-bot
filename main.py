import telebot
from telebot import types
from icrawler.builtin import GoogleImageCrawler
import shutil
import random
import wikipedia
import requests
import datetime

wikipedia.set_lang('ru')

bot = telebot.TeleBot('5502613023:AAFsb-kerhTpeRSCfqh1_zRnOqPCaykbbDM')

markup = types.ReplyKeyboardMarkup()
markup.add(types.KeyboardButton('/help'))
markup.add(types.KeyboardButton("Узнать погоду"))
markup.add(types.KeyboardButton('Узнать информацию по слову из Википедии'))
markup.add(types.KeyboardButton('Подобрать обои на рабочий стол'))
markup.add(types.KeyboardButton('Узнать расписание'))
markup.add(types.KeyboardButton('Полезные ссылки для студента НГТУ'))

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот-помощник) Выбери нужную функцию в меню, и я помогу тебе!", reply_markup=markup)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,"Выбери нужное действие в меню!")

def get_weather(message):
    city = message.text
    open_weather_token = "28c7e1a09c805fa0277d904c486ab90a"
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric&lang=ru")
        data = r.json()
        # pprint(data)

        city = data["name"]
        # description = data["weather"]["description"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        bot.send_message(message.chat.id, f"Погода в городе: {city}\nТемператра воздуха: {temperature}C\n"
                                          f"Ощущается как: {feels_like}\n"
                                          f"Влажность: {humidity}\nДавление: {pressure} мм.рт.ст\nСкорость ветра: {wind}\n"
                                          f"Восход: {sunrise_timestamp}\nЗакат: {sunset_timestamp}")

    except Exception as ex:
        bot.send_message(message.chat.id, 'Ошибка в названии города\nПопробуйте снова')
    bot.send_message(message.chat.id, 'Выберите действие в меню')

def Wallpaper(message):
    bot.send_message(message.chat.id, 'Ожидайте пару секунд)')
    google_crawler = GoogleImageCrawler(storage={'root_dir': 'C:/Users/malig/питон'})
    google_crawler.crawl(keyword=message.text, max_num=3)
    a = random.randint(1, 3)
    try:
        photo = open('C:/Users/malig/питон/00000' + str(a) + '.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)
        photo.close()
    except Exception:
        bot.send_message(message.chat.id, 'Возникла ошибка, попробуйте еще раз')
    path = "C:/Users/malig/питон"
    shutil.rmtree(path)
    bot.send_message(message.chat.id, 'Выберите действие в меню')

def Wikipedia_text(message):
    final_message = " "
    word = message.text.strip().lower()
    try:
        final_message = wikipedia.summary(word)
    except wikipedia.exceptions.PageError:
        final_message = " По вашему запросу ничего не найдено "
    bot.send_message(message.chat.id, final_message, parse_mode='html')
    bot.send_message(message.chat.id, 'Выберите действие в меню')



@bot.message_handler(content_types=['text'])
def start(message):
    if message.text=='Подобрать обои на рабочий стол':
        mesg = bot.send_message(message.chat.id, 'Я бот, который поможет тебе подобрать обои для рабочего стола или просто красивую картинку.Напиши мне слово и я подберу картинку по твоему запросу!')
        bot.register_next_step_handler(mesg, Wallpaper)
    if message.text == 'Узнать информацию по слову из Википедии':
        mess = bot.send_message(message.chat.id,
                                f'Привет, <b>{message.from_user.first_name} {message.from_user.last_name}</b>\n Введите ваш запрос  и я найду статью из Википедии',
                                parse_mode='html')
        bot.register_next_step_handler(mess, Wikipedia_text)

    if message.text == 'Узнать погоду':
        messs = bot.send_message(message.chat.id, "Введите название города")
        bot.register_next_step_handler(messs, get_weather)

    if message.text == 'Полезные ссылки для студента НГТУ':
        buttons = [
            types.InlineKeyboardButton(text="Список преподавателей", url="https://www.nntu.ru/sveden/employees"),
            types.InlineKeyboardButton(text="Четность недели", callback_data='Сейчас лето! Хороших каникул!'),
            types.InlineKeyboardButton(text="Проверить успеваемость", url="https://web.archive.org/web/20211109062603/https://www.nntu.ru/content/studentam/uspevaemost")
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, "Кнопки-ссылки", reply_markup=keyboard)

        @bot.callback_query_handler(func=lambda call: call.data == 'Сейчас лето! Хороших каникул!')
        def callback_inline(call):
            bot.send_message(message.chat.id, 'Сейчас лето! Хороших каникул!')

    if message.text == 'Узнать расписание':
        buttons = [
            types.InlineKeyboardButton(text="1 курс", callback_data='1'),
            types.InlineKeyboardButton(text="2 курс", callback_data='2'),
            types.InlineKeyboardButton(text="3 курс", callback_data='3'),
            types.InlineKeyboardButton(text="4 курс", callback_data='4'),
            types.InlineKeyboardButton(text="5 курс", callback_data='5')
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, "Выберите курс", reply_markup=keyboard)



        @bot.callback_query_handler(func=lambda call: call.data == '1')
        def callback_inline_first(call):
            buttons = [
                types.InlineKeyboardButton(text="ИРИТ",url="https://docs.google.com/spreadsheets/d/1J3d69QH49C96uCix7vat5-qH2WZKfIRT/edit#gid=26020349"),
                types.InlineKeyboardButton(text="ИТС",url="https://docs.google.com/spreadsheets/d/1FFuHQipCE3iEQB6k-iMf7I9UIEinNF-v/edit#gid=1845133819"),
                types.InlineKeyboardButton(text="ИЯЭиТФ",url="https://vk.com/nnstu_ftf"),
                types.InlineKeyboardButton(text="ИНЭЛ",url="https://docs.google.com/spreadsheets/d/1hmVyfTeNKXkDyiBmoTjxJnK6eVGa-sCX/edit#gid=1464892436"),
                types.InlineKeyboardButton(text="ИФХТиМ",url="https://docs.google.com/spreadsheets/d/1cY13jDq64F4yov6ZjKD42_vahTysavO0/edit#gid=1433259151"),
                types.InlineKeyboardButton(text="ИПТМ",url="https://docs.google.com/spreadsheets/d/1qkcDeGdJ8WoCIvPkTFfst8sNv56JtGx6/edit#gid=425044725"),
                types.InlineKeyboardButton(text="ИНЭУ",url="https://vk.com/ineungtu"),
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            bot.send_message(message.chat.id, "Кнопки-ссылки на расписание", reply_markup=keyboard)
        @bot.callback_query_handler(func=lambda call: call.data == '2')
        def callback_inline_second(call):
            buttons = [
                types.InlineKeyboardButton(text="ИРИТ", url="https://docs.google.com/spreadsheets/d/1mmxdRct2KB29ZfgFV-wioSI9MnwJtyqs/edit#gid=1113528126"),
                types.InlineKeyboardButton(text="ИТС",url="https://docs.google.com/spreadsheets/d/1FFuHQipCE3iEQB6k-iMf7I9UIEinNF-v/edit#gid=1845133819"),
                types.InlineKeyboardButton(text="ИЯЭиТФ",url="https://vk.com/nnstu_ftf"),
                types.InlineKeyboardButton(text="ИНЭЛ",url="https://docs.google.com/spreadsheets/d/1hmVyfTeNKXkDyiBmoTjxJnK6eVGa-sCX/edit#gid=1464892436"),
                types.InlineKeyboardButton(text="ИФХТиМ",url="https://docs.google.com/spreadsheets/d/1cY13jDq64F4yov6ZjKD42_vahTysavO0/edit#gid=1433259151"),
                types.InlineKeyboardButton(text="ИПТМ",url="https://docs.google.com/spreadsheets/d/1qkcDeGdJ8WoCIvPkTFfst8sNv56JtGx6/edit#gid=425044725"),
                types.InlineKeyboardButton(text="ИНЭУ",url="https://vk.com/ineungtu"),
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            bot.send_message(message.chat.id, "Кнопки-ссылки на расписание", reply_markup=keyboard)

        @bot.callback_query_handler(func=lambda call: call.data == '3')
        def callback_inline_third(call):
            buttons = [
                types.InlineKeyboardButton(text="ИРИТ",url="https://docs.google.com/spreadsheets/d/1dsrxSTJ-xuSbp5tYEZ59qUi9_IuSGBdK/edit#gid=1802215083"),
                types.InlineKeyboardButton(text="ИТС",url="https://docs.google.com/spreadsheets/d/1FFuHQipCE3iEQB6k-iMf7I9UIEinNF-v/edit#gid=1845133819"),
                types.InlineKeyboardButton(text="ИЯЭиТФ",url="https://vk.com/nnstu_ftf"),
                types.InlineKeyboardButton(text="ИНЭЛ",url="https://docs.google.com/spreadsheets/d/18Y5JU4_IZnz4CLlUTjIAsqV4v5u8CWm7/edit#gid=341398593"),
                types.InlineKeyboardButton(text="ИФХТиМ",url="https://docs.google.com/spreadsheets/d/1nf9jYVld--MZ-CswfkzoGjASGG3PGoNn/edit#gid=2111385652"),
                types.InlineKeyboardButton(text="ИПТМ",url="https://docs.google.com/spreadsheets/d/1DcnWTg81G6qOw1MjuoW3EHUTNgnBI82M/edit#gid=1162863141"),
                types.InlineKeyboardButton(text="ИНЭУ",url="https://vk.com/ineungtu"),
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            bot.send_message(message.chat.id, "Кнопки-ссылки на расписание", reply_markup=keyboard)

        @bot.callback_query_handler(func=lambda call: call.data == '4')
        def callback_inline_four(call):
            buttons = [
                types.InlineKeyboardButton(text="ИРИТ",url="https://docs.google.com/spreadsheets/d/1GiGh8Yc2xwlXjX3xkMZTI0IU-duxCFQQ/edit#gid=2007860904"),
                types.InlineKeyboardButton(text="ИТС",url="https://docs.google.com/spreadsheets/d/1FFuHQipCE3iEQB6k-iMf7I9UIEinNF-v/edit#gid=1845133819"),
                types.InlineKeyboardButton(text="ИЯЭиТФ",url="https://vk.com/nnstu_ftf"),
                types.InlineKeyboardButton(text="ИНЭЛ",url="https://docs.google.com/spreadsheets/d/1Q6M7g_qkt-Lncj-yX2qyqe21CIIFjczS/edit#gid=2125922402"),
                types.InlineKeyboardButton(text="ИФХТиМ",url="https://docs.google.com/spreadsheets/d/1nf9jYVld--MZ-CswfkzoGjASGG3PGoNn/edit#gid=2111385652"),
                types.InlineKeyboardButton(text="ИПТМ",url="https://docs.google.com/spreadsheets/d/1DcnWTg81G6qOw1MjuoW3EHUTNgnBI82M/edit#gid=1162863141"),
                types.InlineKeyboardButton(text="ИНЭУ",url="https://vk.com/ineungtu"),
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            bot.send_message(message.chat.id, "Кнопки-ссылки на расписание", reply_markup=keyboard)


        @bot.callback_query_handler(func=lambda call: call.data == '5')
        def callback_inline_four(call):
            buttons = [
                types.InlineKeyboardButton(text="ИРИТ",url="https://docs.google.com/spreadsheets/d/1QEGTgmpK39AmPL3DbUPMPCHdH-CLQa9j/edit#gid=1333036647"),
                types.InlineKeyboardButton(text="ИТС",url="https://docs.google.com/spreadsheets/d/1FFuHQipCE3iEQB6k-iMf7I9UIEinNF-v/edit#gid=1845133819"),
                types.InlineKeyboardButton(text="ИЯЭиТФ",url="https://vk.com/nnstu_ftf"),
                types.InlineKeyboardButton(text="ИНЭЛ",url="такого курса нет"),
                types.InlineKeyboardButton(text="ИФХТиМ",url="https://docs.google.com/spreadsheets/d/1nf9jYVld--MZ-CswfkzoGjASGG3PGoNn/edit#gid=2111385652"),
                types.InlineKeyboardButton(text="ИПТМ",url="https://docs.google.com/spreadsheets/d/1DcnWTg81G6qOw1MjuoW3EHUTNgnBI82M/edit#gid=1162863141"),
                types.InlineKeyboardButton(text="ИНЭУ",url="https://vk.com/ineungtu"),
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            bot.send_message(message.chat.id, "Кнопки-ссылки на расписание", reply_markup=keyboard)

bot.polling(none_stop=True)