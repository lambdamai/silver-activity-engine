import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from cleantext import clean
import re
import json
import os
import sys
import logging
import subprocess

base_url = 'https://www.rusprofile.ru/codes/'

org_activity_codes = [
    561000,
    471100,
    562900,
    563000,

]

logging.basicConfig(filename='log.log', filemode='w', level=logging.INFO)

def process_page(soup):
    orgs = []
    for org in soup.findAll('div', class_='company-item'):
        title = clean(org.find('a').get_text(), lower=True)
        link = org.find('a')['href']

        head_title = clean(org.select_one('.company-item-info>dl>dt').get_text(), lower=True)
        head_name = clean(org.select_one('.company-item-info>dl>dd').get_text(), lower=True)

        address = clean(org.find('address').get_text(), lower=True)

        inn = clean(org.find(text="ИНН").parent.parent.findNext('dd').get_text(), lower=True)
        ogrn = clean(org.find(text="ОГРН").parent.parent.findNext('dd').get_text(), lower=True)
        reg_date = clean(org.find(text="Дата регистрации").parent.parent.findNext('dd').get_text(), lower=True)
        reg_cap_dirty = org.find(text="Уставный капитал")
        reg_cap = clean(reg_cap_dirty.parent.parent.findNext('dd').get_text(), lower=True) if reg_cap_dirty != None else None

        status = org.select_one('.warning-text, .attention-text')
        if status != None:
            status = clean(status.get_text(), lower=True)

        main_activity = clean(org.find(text="Основной вид деятельности").parent.parent.findNext('dd').get_text(), lower=True)
        main_activity_code = int(re.findall(r'\d+', main_activity.replace('.', ''))[0].ljust(6, '0'))
        
        if status == 'Организация ликвидирована':
            return (orgs, False)

        orgs.append({
            'title': title,
            'link': link,
            'head_title': head_title,
            'head_name': head_name,
            'inn' : inn,
            'ogrn': ogrn,
            'reg_date': reg_date,
            'reg_cap': reg_cap,
            'status': status,
            'main_activity': main_activity,
            'main_activity_code': main_activity_code,
            'address': address
            })

    return (orgs, True)


s = requests.Session()

for code in org_activity_codes:
    page_num = 1
    is_next_page = True

    while is_next_page: 
        sys.stdout.flush()

        if page_num > 100:
            break

        print(f'Processing {code} page {page_num}.')
        url = base_url + str(code) + '/' + str(page_num)
        #resp = s.get(url, verify=False, cookies={'okved_all':'yes'})
        resp = s.get(url, verify=False)

        if resp.status_code != 200:
            is_next_page = False
            logging.info(f'[Status not 200.] [STOP] {url}')
            break

        page = resp.text

        soup = BeautifulSoup(page, 'html.parser') 

        is_busted = False
        if soup.find('form', id='checkform'):
            is_busted = True
            logging.info(f'[Capcha.] {url}')
            subprocess.run(['firefox.exe', '-new-instance', url])
            continue

        cout_text = soup.find('span', class_='okved-company-tools__label').get_text()
        count = int(re.findall(r'\d+', cout_text)[-1])

        print(f'pages {(count // 100) + 1}')

        if page_num > (count // 100) + 1:
            is_next_page = False
            logging.info(f'[Last page.] [STOP] {url}')
            break

        (orgs, is_next_page) = process_page(soup)

        file_name = f'out\\{code}\\{page_num}.json'
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name, 'w', encoding="utf-8") as out_file:
            out_file.write(json.dumps(orgs, indent=3, ensure_ascii=False))

        if is_next_page == False:
            logging.info(f'[Found liqidated organization.] [STOP] {url}')
            break

        page_num += 1

        time.sleep(6)