import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import requests
from bs4 import BeautifulSoup
import re

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
        dates.append([int(yyyy)*10000 + int(mm)*100 + int(dd), i, j])
        
dates = sorted(dates, key = lambda element: element[0], reverse = True)

notification_object = objects[dates[0][1]][dates[0][2]]

category = categories[dates[0][1]].find('h3', 'list-title').text
title = notification_object.find('div', 'item-title').text
link = 'https://www.csie.ncu.edu.tw' + notification_object['href']
date = notification_object.find('div', 'item-time').text

print('NCUCS佈告欄\n\n{}\n\n{}: {}\n{}'.format(date, category, title, link))

path = 'news'

titles = []

try:
    collection_ref = database.collection(path)

    docs = collection_ref.get()

    for doc in docs:
        titles.append(doc.to_dict()['title'])

    if title not in titles:
        doc_to_add = {
            'category': category,
            'title': title,
            'link': link,
            'date': date
            }
            
    collection_ref.add(doc_to_add)

except:
    pass