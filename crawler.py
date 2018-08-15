import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import requests
from bs4 import BeautifulSoup
import re
import os
import telebot

bot = telebot.TeleBot(os.environ['access_token'])

with open('serviceAccount.json', 'w') as f:
    f.write(os.environ['serviceAccount'])

cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred)

database = firestore.client()

url = 'https://www.csie.ncu.edu.tw/'
resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'html.parser')

categories = soup.find_all('div', 'announcement-scope')
objects = [info.find_all('a', 'link') for info in categories]

dates = []

for i in range(len(categories)):
    for j in range(len(objects[i])):
        yyyy, mm, dd = objects[i][j].find('div', 'item-time').text.split('-')
        dates.append([int(yyyy)*10000 + int(mm)*100 + int(dd), objects[i][j].find('div', 'item-time').text, categories[i].find('h3', 'list-title').text, objects[i][j].find('div', 'item-title').text, 'https://www.csie.ncu.edu.tw' + objects[i][j]['href']])
        
dates = sorted(dates, key = lambda element: element[0], reverse = True)

path = 'news'

titles = []

collection_ref = database.collection(path)

docs = collection_ref.get()

for doc in docs:
    titles.append(doc.to_dict()['title'])

for i in range(len(dates)):

    date = dates[1]
    category = dates[2]
    title = dates[3]
    link = dates[4]

    notification = 'NCUCS佈告欄\n\n{}\n\n{}: {}\n{}'.format(date, category, title, link)

    if title in titles:

        break

    else:

        print(notification)

        doc_to_add = {
            'category': category,
            'title': title,
            'link': link,
            'date': date
            }

        collection_ref.add(doc_to_add)

        ids = []

        ids_doc = database.collection('users').get()

        for id_doc in ids_doc:
            ids.append(id_doc.to_dict()['id'])

        for id in ids:
            bot.send_message(id, notification)