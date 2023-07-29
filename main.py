import telebot
import sqlite3
from telebot import types

bot = telebot.TeleBot('6196338780:AAGB2AQ4IAIyuKkWE8s71i3pbJ-IhGzQZtk')
name = None

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Інформація')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Асорті')
    btn3 = types.KeyboardButton('Промокод')
    btn4 = types.KeyboardButton('Доставка')
    markup.row(btn2, btn3, btn4)
    btn5 = types.KeyboardButton('Сховище')
    markup.row(btn5)
    bot.reply_to(message, f'Привіт {message.from_user.first_name}, напиши мені, що тебе цікавить одним словом наприклад : асорті, або вибери відповідну кнопку', reply_markup=markup)

@bot.message_handler(commands=['Оформити'])
def start(message):
    conn = sqlite3.connect('clients.sql') #де зберігається база даних
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users(id int auto_increment primary key, name varchar(150), about varchar(255))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.from_user.id, "Введіть Ваше ім'я та номер телефону, якщо Ви не туди клацнули введіть '-' ")
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.from_user.id, "Напишіть нам що ви бажаєте замовити, а також, самовивіз або куди доставляти НП(на території всієї України), якщо Ви нетуди клацнули введіть '-' ")
    bot.register_next_step_handler(message, user_about)

def user_about(message):
    order = message.text.strip()

    conn = sqlite3.connect('clients.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name, about) VALUES ('%s', '%s')" % (name, order))
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    bot.send_message(message.from_user.id, 'Успішно, очікуйте на відповідь! Мирного неба! Слава Україні!', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback (call):
    conn = sqlite3.connect('clients.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    info = ''
    for el in users:
        info += f'Імя та номер телефону : {el[1]}.\n Замовлення : {el[2]}.\n\n\n'

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)

@bot.message_handler()
def info(message):
    if message.text.lower() == 'привіт':
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Інформація')
        markup.row(btn1)
        btn2 = types.KeyboardButton('Асорті')
        btn3 = types.KeyboardButton('Промокод')
        btn4 = types.KeyboardButton('Доставка')
        markup.row(btn2, btn3, btn4)
        btn5 = types.KeyboardButton('Сховище')
        markup.row(btn5)
        bot.send_message(message.from_user.id, f'Привіт {message.from_user.first_name}, напиши мені, що тебе цікавить одним словом, наприклад : асорті, або вибери відповідну кнопку', reply_markup=markup)

    elif message.text.lower() == 'інформація':
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Асорті')
        btn2 = types.KeyboardButton('Головна')
        markup.row(btn1, btn2)
        bot.send_message(message.from_user.id, f'З нами ви отримаєте:🍿 Свіжий та хрусткий попкорн, з приголомшливим асортиментом смаків.🍿 Найкраще співвідношення ціни та якості🍿 Атмосферу затишку та радості кожного разу, коли розпаковуєте наш попкорн. Ми не тільки любимо попкорн, а й створюємо магію кожного кадру. 🌟 Приєднуйтесь до нас тут, щоб бути в курсі новин, акцій та розіграшів! Ми обіцяємо поділитися ексклюзивними промокодами та особистими знижками для наших шанувальників. Не забудьте поділитися з друзями які теж люблять смачний попкорн. Дякуємо за вашу підтримку і разом створимо незабутні моменти. Також не забуваємо за наших захисників❤️💪, відправляємо з кожного замовлення 5% на ЗСУ', reply_markup=markup)

    elif message.text.lower() == 'асорті':
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Сирний')
        btn2 = types.KeyboardButton('Карамельний')
        markup.row(btn1, btn2,)
        btn3 = types.KeyboardButton('Шоколадний')
        btn4 = types.KeyboardButton('/Оформити')
        markup.row(btn3, btn4)
        btn5 = types.KeyboardButton('Головна')
        markup.row(btn5)
        file = open('./Asorti.jpg', 'rb')
        bot.send_photo(message.from_user.id, file, reply_markup=markup)
        bot.send_message(message.from_user.id, 'В наявності є сирний, карамельний та шоколадний попкорн, напишіть мені лише смак, який Вас цікавить, або виберіть відповідну кнопку, якщо Ви бажаєте оформити замовленя, напишіть мені /оформити, або виберіть відповідну кнопку', reply_markup=markup)

    elif message.text.lower() == 'сирний':
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Асорті')
        btn2 = types.KeyboardButton('/Оформити')
        markup.row(btn1, btn2)
        btn3 = types.KeyboardButton('Головна')
        markup.row(btn3)
        file = open('./Asorti/Chese.jpg', 'rb')
        bot.send_photo(message.from_user.id, file, reply_markup=markup)
        bot.send_message(message.from_user.id, 'Його ціна 110 грн за 0.5кг, бажаєте оформити замовлення?', reply_markup=markup)

    elif message.text.lower() == 'карамельний':
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Асорті')
        btn2 = types.KeyboardButton('/Оформити')
        markup.row(btn1, btn2)
        btn3 = types.KeyboardButton('Головна')
        markup.row(btn3)
        file = open('./Asorti/Caramel.jpg', 'rb')
        bot.send_photo(message.from_user.id, file, reply_markup=markup)
        bot.send_message(message.from_user.id, 'Його ціна 115 грн за 0.5кг, бажаєте оформити замовлення?', reply_markup=markup)

    elif message.text.lower() == 'шоколадний':
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Асорті')
        btn2 = types.KeyboardButton('/Оформити')
        markup.row(btn1, btn2)
        btn3 = types.KeyboardButton('Головна')
        markup.row(btn3)
        file = open('./Asorti/Chocolate.jpg', 'rb')
        bot.send_photo(message.from_user.id, file, reply_markup=markup)
        bot.send_message(message.from_user.id, 'Його ціна 130 грн за 0.5кг, бажаєте оформити замовлення?', reply_markup=markup)

    elif message.text.lower() == 'оформити':
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('/Оформити')
        btn2 = types.KeyboardButton('Асорті')
        markup.row(btn1, btn2)
        btn3 = types.KeyboardButton('Головна')
        markup.row(btn3)
        bot.send_message(message.from_user.id, 'введіть /Оформити', reply_markup=markup)

    elif message.text.lower() == 'головна':
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Інформація')
        markup.row(btn1)
        btn2 = types.KeyboardButton('Асорті')
        btn3 = types.KeyboardButton('Промокод')
        markup.row(btn2, btn3)
        btn4 = types.KeyboardButton('Сховище')
        btn5 = types.KeyboardButton('Доставка')
        markup.row(btn4, btn5)
        bot.send_message(message.from_user.id, f'Привіт {message.from_user.first_name}, напиши мені, що тебе цікавить одним словом, наприклад : асорті, або вибери відповідну кнопку', reply_markup=markup)

    elif message.text.lower() == 'промокод':
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Асорті')
        btn2 = types.KeyboardButton('/Оформити')
        markup.row(btn1, btn2)
        btn3 = types.KeyboardButton('Головна')
        markup.row(btn3)
    #    file = open('./sale10.jpg', 'rb')
    #   bot.send_photo(message.chat.id, file, reply_markup=markup)
    #    bot.reply_to(message, f'Знижка 10% за промокодом : Popcornix HMibot', reply_markup=markup)
        bot.send_message(message.from_user.id, f'Немає доступних промокодів.', reply_markup=markup)

    elif message.text.lower() == 'доставка':
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('/Оформити')
        btn2 = types.KeyboardButton('Асорті')
        markup.row(btn1, btn2)
        btn3 = types.KeyboardButton('Головна')
        markup.row(btn3)
        bot.send_message(message.from_user.id, f'Відправляємо НП, а також, можливий самовивіз : м.Збараж, вул. Я.Мудрого 4 (біля 2-ї школи) або Котляревського 5 (біля Базаринецької церкви)', reply_markup=markup)

    elif message.text.lower() == 'сховище':
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('/Оформити')
        btn2 = types.KeyboardButton('Асорті')
        markup.row(btn1, btn2)
        btn3 = types.KeyboardButton('Головна')
        markup.row(btn3)
        bot.send_message(message.from_user.id, 'Залишилось : 0.5кг сирного, 1.5кг карамельного та 1.5 кг шоколадного попкорну.', reply_markup=markup)

    elif message.text.lower() == 'адмін-панель_управління-чат_ботом-список_замовлення':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Список', callback_data='users'))
        bot.send_message(message.from_user.id, 'Ось всі замовлення :', reply_markup=markup)



bot.polling(none_stop=True)