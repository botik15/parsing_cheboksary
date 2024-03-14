import time

import requests
from bs4 import BeautifulSoup
import datetime
import telebot
import os
import configparser

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("settings.ini")  # читаем конфиг
'''
[settings]
token_chatgtp = *******
chat_id = *******
token_telegram = *******
message_id = *******
'''


url = 'https://afisha.cheb.ru/kino/?cdate=' + str(datetime.date.today()) + '&cfilms='
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
i = 0

for items in soup.find_all('div', class_='showfilm'):
    for item in items.find_all('tr'):
        name_films = ''
        img_href = ''
        opisanie = ''
        link_name = ''
        cat_time = ''
        time1 = ''
        time2 = ''
        time2_href = ''
        time3 = ''
        time4 = ''

        if item.find('em') is not None:
            name_films = item.find_all_next(string=True)[0]  # Ссылка на имя фильма
            img_href = item.find("a").get('href').replace('//','')  # Ссылка на картинку
            opisanie = item.find('em').text.replace('\n', 's')  # Ссылка на описение
            link_name = item.find_all('td', class_='cfilms_img')[0].find_all('a')[1].get('href').replace('//','')  # Ссылка на сам фильм
            cat_time = item.find('span').find_all_next(string=True)[0]
            x = (f"Название: {name_films}\nКатегория: {cat_time.partition(')')[0:][0].replace('(','')}\nПродолжительность: {cat_time.partition(')')[-1:][0]}\n\nОписание: {opisanie}\n\nПодробнее: {link_name}\n\n")
            ss = []
            for i in item.find_all('table', 'cfilms_table')[0].find_all('tr'):
                try:
                    time1 = i.find('td', class_='cfilms_1').text
                    time2 = i.find('td', class_='cfilms_2').text
                    time2_href = i.find('td', class_='cfilms_2').find('a').get('href')
                    time3 = i.find('td', class_='cfilms_3').text
                    time4 = i.find('td', class_='cfilms_4').text
                    ss.append(f"Начало в : {time1}\nКинотеатр: {time2}\nЗал: {time3}\nЦена: {time4}\n\n")
                except:
                    pass

            with open('db.txt', 'r', encoding='utf8') as f_r:
                line = f_r.readlines()[0]
                if line.find(link_name) == -1:
                    with open('db.txt', 'a', encoding='utf8') as f:
                        f.write(link_name)
                        bot.send_photo(chat_id='-1001820906851',photo= img_href , caption=x )
                        print('Добавил - ' + x)
                        time.sleep(5)
                else:
                    print('no')


