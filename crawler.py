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


def ncu_cs_crawler():

    url = 'https://www.csie.ncu.edu.tw/'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    categories = soup.find_all('div', 'announcement-scope')
    objects = [info.find_all('a', 'link') for info in categories]

    result = []

    for i in range(len(categories)):
        for j in range(len(objects[i])):
            yyyy, mm, dd = objects[i][j].find('div', 'item-time').text.split('-')
            result.append([int(yyyy)*10000 + int(mm)*100 + int(dd), objects[i][j].find('div', 'item-time').text, categories[i].find('h3', 'list-title').text, objects[i][j].find('div', 'item-title').text, 'https://www.csie.ncu.edu.tw' + objects[i][j]['href']])

    return result

def ncu_fresh_crawler():

    url = 'https://ncufresh.ncu.edu.tw/'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    category = '新生知訊網'
    objects = soup.find_all('tr', 'news-row open-modal')

    result = []

    dates = [infos.find('td', 'news-time open-modal').text for infos in objects]
    links = ['https://ncufresh.ncu.edu.tw/require_data/?id={}'.format(infos['id']) for infos in objects]
    titles = [infos.find('p', 'dotdotdottext open-modal').text for infos in objects]

    for i in range(len(titles)):
        yyyy, mm, dd = dates[i].split('-')
        result.append([int(yyyy)*10000 + int(mm)*100 + int(dd), dates[i], category, titles[i], links[i]])

    return result

def ncu_dorm_crawler():

    url = 'http://in.ncu.edu.tw/ncu7221/OSDS/'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    category = '宿舍公告'

    result = []

    dates = []
    titles = []
    links = []

    for i in range(len(soup.find_all('div', align = 'center'))):
        match = re.search('\\d\\d\\d\\d-\\d\\d-\\d\\d', str(soup.find_all('div', align = 'center')[i]))
        if match:
            dates.append(match.group(0))

    for i in range(len(soup.find_all('a'))):
        match = re.search('post_detail.php\\?no=(.*)">(.*)<', str(soup.find_all('a')[i]))
        if match:
            titles.append(match.group(2))
            links.append('http://in.ncu.edu.tw/ncu7221/OSDS/post_detail.php?no=' + str(match.group(1)))

    for i in range(len(titles)):
        yyyy, mm, dd = dates[i].split('-')
        result.append([int(yyyy)*10000 + int(mm)*100 + int(dd), dates[i], category, titles[i], links[i]])

    return result

def ust_crawler():

    url = 'http://www.ust.edu.tw/News.aspx'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    category = '臺聯大系統'

    result =[]

    dates = []
    titles = []
    links = []

    for i in range(len(soup.find_all('span'))):
        match = re.search('\\d\\d\\d\\d-\\d{1,2}-\\d{1,2}', str(soup.find_all('span')[i]))
        if match:
            dates.append(match.group(0))

    for i in range(len(soup.find_all('a'))):
        match = re.search('GUID=(.*)" id=(.*)">(.*)<', str(soup.find_all('a')[i]))
        if match:
            titles.append(match.group(3))
            links.append('http://www.ust.edu.tw/News_Detailed.aspx?GUID=' + str(match.group(1)))

    for i in range(len(titles)):
        yyyy, mm, dd = dates[i].split('-')
        result.append([int(yyyy)*10000 + int(mm)*100 + int(dd), dates[i], category, titles[i], links[i]])

    return result

def ncu_oaa_crawler():

    url = 'http://pdc.adm.ncu.edu.tw/news00.asp'
    resp = requests.get(url)
    resp.encoding = 'big5'
    soup = BeautifulSoup(resp.text, 'html.parser')

    category = '教務處'

    result = []

    dates = []
    titles = []
    links = []

    for i in range(len(soup.find_all('td', 'copy'))):
        match = re.search('\\d\\d\\d\\d.\\d{1,2}.\\d{1,2}', str(soup.find_all('td', 'copy')[i]))
        if match:
            dates.append(match.group(0).replace('.', '-'))

    for i in range(len(soup.find_all('a'))):
        match = re.search('^<a href="(.*)" onfocus=(.*)">(.*)</f', str(soup.find_all('a')[i]))
        if match:
            titles.append(match.group(3))
            if re.search('^news_detail.aspx(.*)', str(match.group(1))):
                links.append('http://pdc.adm.ncu.edu.tw/' + str(match.group(1)))
            else:
                links.append(str(match.group(1)))            

    for i in range(len(titles)):
        yyyy, mm, dd = dates[i].split('-')
        result.append([int(yyyy)*10000 + int(mm)*100 + int(dd), dates[i], category, titles[i], links[i]])

    return result

def ncu_osa_crawler():

    url = 'http://osa.ncu.edu.tw/'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    category = '學務處'

    objects = soup.find_all('td', style = 'background:url(images/color-01gray.gif) top repeat-x; padding:9px 10px 9px')

    result = []

    dates = [re.search('\\d\\d\\d\\d-\\d{1,2}-\\d{1,2}', infos.find('font', 'note').text).group(0) for infos in objects]
    titles = [infos.find('a').text for infos in objects]
    links = ['http://osa.ncu.edu.tw/' + infos.find('a')['href'] for infos in objects]

    for i in range(len(titles)):
        yyyy, mm, dd = dates[i].split('-')
        result.append([int(yyyy)*10000 + int(mm)*100 + int(dd), dates[i], category, titles[i], links[i]])
    
    return result

def ncu_oga_crawler():

    url = 'http://oga.ncu.edu.tw/ncuoga/oga/index.php'
    resp = requests.get(url)
    resp.encoding = 'big5'
    soup = BeautifulSoup(resp.text, 'html.parser').find('div', 'content1-container-1col')

    category = '總務處'

    result = []

    dates = []
    titles = []
    links = []

    for i in range(len(soup.find_all('td'))):
        match = re.search('\\d\\d\\d\\d-\\d{1,2}-\\d{1,2}', str(soup.find_all('td')[i]))
        if match:
            dates.append(match.group(0))

    for i in range(len(soup.find_all('a'))):
        titles.append(soup.find_all('a')[i].text)
        links.append('http://oga.ncu.edu.tw/ncuoga/oga/' + soup.find_all('a')[i]['href'])     

    for i in range(len(titles)):
        yyyy, mm, dd = dates[i].split('-')
        result.append([int(yyyy)*10000 + int(mm)*100 + int(dd), dates[i], category, titles[i], links[i]])

    return result
    

notifications = ncu_cs_crawler() + ncu_fresh_crawler() + ncu_dorm_crawler() + ust_crawler() + ncu_oaa_crawler() + ncu_osa_crawler()

notifications = sorted(notifications, key = lambda element: element[0], reverse = True)

path = 'news'

titles = []

collection_ref = database.collection(path)

docs = collection_ref.get()

for doc in docs:
    titles.append(doc.to_dict()['title'])

for i in range(len(notifications)):

    date = notifications[i][1]
    category = notifications[i][2]
    title = notifications[i][3]
    link = notifications[i][4]

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