import os
import telebot
from flask import Flask, request
import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


TOKEN = os.environ['access_token'].strip()
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


def newtalk_top_5():

    reply = 'NewTalk 即時新聞 TOP 5\n\n'

    url = 'http://newtalk.tw/news/summary/today'
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html.parser')

    newtalk_block_1 = soup.find_all('div', 'news-title')
    newtalk_block_2 = soup.find_all('div', 'text col-md-8 col-sm-8 col-xs-6')

    newtalk_article = []

    for i in range(2):
        newtalk_article.append([newtalk_block_1[i].text, newtalk_block_1[i].find('a')['href']])

    for i in range(3):
        newtalk_article.append([newtalk_block_2[i].find('div', 'news_title').text.strip(), newtalk_block_2[i].find('a')['href']])
    
    for index, item in enumerate(newtalk_article):
        reply += '{}. {}\n{}\n\n'.format(index + 1, item[0], item[1])

    reply += '離開: /leave'

    return reply


def ptt_top_5():

    reply = 'PTT 熱門文章 TOP 5\n\n'

    url = 'https://disp.cc/m/'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    ptt_titles = soup.find_all('div', 'ht_title')
    ptt_links = soup.find_all('a')

    ptt_article = []

    for i in range(5):
        ptt_article.append([ptt_titles[i].text, 'https://disp.cc/m/' + ptt_links[i]['href']])
    
    for index, item in enumerate(ptt_article):
        reply += '{}. {}\n{}\n\n'.format(index + 1, item[0], item[1])

    reply += '離開: /leave'
    
    return reply


def dcard_top_5():

    reply = 'Dcard 熱門文章 Top 5\n\n'

    url = 'https://www.dcard.tw/f'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    dcard_titles = soup.find_all('h3', 'PostEntry_title_H5o4d PostEntry_unread_2U217')
    dcard_links = soup.find_all('a', 'PostEntry_root_V6g0r')

    dcard_article = []

    for i in range(5):
        dcard_article.append([dcard_titles[i].text, 'https://www.dcard.tw' + dcard_links[i]['href']])
    
    for index, item in enumerate(dcard_article):
        reply += '{}. {}\n{}\n\n'.format(index + 1, item[0], item[1])

    reply += '離開: /leave'
    
    return reply

def get_user_id(user_id):

    print(user_id)

    cred = credentials.Certificate(os.environ['serviceAccount'])

    firebase_admin.initialize_app(cred)

    database = firestore.client()

    path = 'users'

    ids = []

    try:
        docs = database.collection(path).get()

        for doc in docs:
            ids.append(doc.to_dict()['id'])

        if user_id not in ids:
            doc_to_add = {
                'id': user_id
            }

            doc_ref = database.document(path + '/user_' + str(user_id))
            doc_ref.set(doc_to_add)
    except:
        pass


@bot.message_handler(commands=['start', 'leave'])
def start(message):
    get_user_id(str(message.chat.id))
    print('command: /start')
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name + '.\nHere are some functions:\n/start\n/newtalk_top_5\n/ptt_top_5\n/dcard_top_5')


@bot.message_handler(commands=['newtalk_top_5'])
def get_newtalk_top_5(message):
    get_user_id(str(message.chat.id))
    print('command: /newtalk_top_5')
    bot.reply_to(message, newtalk_top_5())


@bot.message_handler(commands=['ptt_top_5'])
def get_ptt_top_5(message):
    get_user_id(str(message.chat.id))
    print('command: /ptt_top_5')
    bot.reply_to(message, ptt_top_5())


@bot.message_handler(commands=['dcard_top_5'])
def get_dcard_top_5(message):
    get_user_id(str(message.chat.id))
    print('command: /dcard_top_5')
    bot.reply_to(message, dcard_top_5())


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    get_user_id(str(message.chat.id))
    print(message.text)
    bot.reply_to(message, message.text)


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://telebot-20180812.herokuapp.com/callback' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))