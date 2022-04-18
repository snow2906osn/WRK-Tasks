import requests
import csv
import random
import time
import re
from bs4 import BeautifulSoup

#1. OCR
#pip install pytesseract
#|| from AbbyyOnlineSdk import *
##OCR по картинкам не делается...
#2. WebDriver
#pip install selenium
##нет имитации работы человека...
#3. архивы и бинарные форматы не смотрим...wish list...

# Обработчик картинок и документов не требуется, берем либо https или /ru /en
# Картинки лежат в /_html/img/
# Документы в /upload/iblock

# вероятно с номерами страниц какое-то нае...хитрость https://p4s.biz/ru/media/video/?page=730
# отключим такие узлы (and 'page=' not in v_tstlnk)...можно открыть многотысячные страницы. надо изучать ресурс, а время органичено...
# установив где-то перечень ссылок возможно сделали "защиту" от web-scraping

# Список доступных URL...во избежании....
#v_urlcsv = {'https://sustainability.p4s.biz/': 1, 'https://p4s.biz/': 1}
v_urlcsv = {'https://p4s.biz/': 1}
#with open('allow_urls.txt', newline='') as f_csvurl:
#    v_urlcsv = list(csv.reader(f_csvurl))
v_lckurl = {'<--->': 1}

# Получим дедупликацию
v_emails = {'<--->': 1}

# Блок N 519-ФЗ от 30.12.2020
# https://github.com/N0taN3rd/userAgentLists/blob/master/csv/internet-explorer.csv
# https://t.me/c/1434787269/1622 (proxy.zip)

# Test url = "https://showip.net/"
# text = requests.get('https://showip.net/', proxies=v_soc, headers=v_head).text
with open('ano-ua.txt', newline='') as f_csvua:
    v_uacsv = list(csv.reader(f_csvua))
with open('ano-prx.txt', newline='') as f_csvprx:
    v_prxcsv = list(csv.reader(f_csvprx))
def https_attrib(v_lng = 'ru-RU'):
    v_ua = ''.join(v_uacsv[random.randrange(0, (len(v_uacsv) - 1) if len(v_uacsv) > 1 else 1)])     #Смысл в нескольких useragent. 1 мало (для randrange 0,0 - ошибка)
    v_prx = ''.join(v_prxcsv[random.randrange(0, (len(v_prxcsv) - 1) if len(v_prxcsv) > 1 else 1)]) #Смысл в нескольких socks5. 1 мало (для randrange 0,0 - ошибка)
    v_sleep = random.randrange(0, 9)
    ###v_sleep = random.randrange(0, 3)
    # en-US
    v_head = {'User-Agent': v_ua, 'Accept-Language': v_lng}
    v_soc = {'http': v_prx, 'https': v_prx}
    return v_sleep, v_head, v_soc;

def url_get(v_lng = 'ru-RU', v_domain = 'https://p4s.biz/', v_fullurl='https://p4s.biz/'):
    v_prslnk = {'<--->': 1}
    if v_domain in v_urlcsv and v_fullurl not in v_lckurl:
        vi_sleep, vi_head, vi_soc = https_attrib(v_lng)
        v_lckurl[v_fullurl] = 1
        time.sleep(vi_sleep)
        html = requests.get(v_fullurl, proxies=vi_soc, headers=vi_head).text
        soup = BeautifulSoup(html, 'html.parser')
        # Т.к. https:// могут быть домены N уровня... проверим разрешение на web scraping...
        for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
            v_tstlnk = link.get('href')
            if v_tstlnk not in v_lckurl:
                for key, value in v_urlcsv.items():
                    if v_tstlnk.startswith(key) == True:
                        v_prslnk[v_tstlnk] = 1
        # В данном блоке только те, домены которых разрешены...
        # вероятно с номерами страниц какое-то нае... https://p4s.biz/ru/media/video/?page=730
        # отключим такие узлы
        for link in soup.find_all('a', attrs={'href': re.compile("^/ru" if v_lng == 'ru-RU' else "^/en")}):
            v_tstlnk = v_domain.rstrip('/') + link.get('href')
            if v_tstlnk not in v_lckurl and 'page=' not in v_tstlnk:
                v_prslnk[v_tstlnk] = 1
        # Базовый сбор...
        for link in soup.find_all('a', attrs={'href': re.compile("^mailto:")}):
            v_emails[link.get('href').lstrip('mailto:')] = 1
    return v_prslnk;

def webscraping(v_lng = 'ru-RU', v_domain = 'https://p4s.biz/', v_fullurl='https://p4s.biz/'):
    v_gopath = url_get(v_lng, v_domain, v_fullurl)
    print(v_fullurl)
    for v_fkey, v_fval in v_gopath.items():
        for v_dom, v_dval in v_urlcsv.items():
            if v_fkey.startswith(v_dom) == True:
                webscraping(v_lng, v_dom, v_fkey)

webscraping('ru-RU', 'https://p4s.biz/', 'https://p4s.biz/')
webscraping('en-US', 'https://p4s.biz/', 'https://p4s.biz/')

# Сохраним все в файл
with open('emails.txt', 'w') as emails_file:
    for key, value in v_emails.items():
        if key != '<--->':
            emails_file.write('%s\n' % (key))