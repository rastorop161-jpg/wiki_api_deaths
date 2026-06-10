import requests
from datetime import datetime
import re
from bs4 import BeautifulSoup

def main():

    year = '2026'
    url = f'https://ru.wikipedia.org/wiki/Список_умерших_в_{year}_году'
    headers = {'User-Agent': 'wiki_deaths_bot/1.0 (Rastorop161, rastorop161@gmail.com, https://github.com/rastorop161-jpg) study_project'}
   
    try:
    
        response = requests.get(url, headers = headers, timeout = 30)
        
        if response.status_code != 200:
            print(f'Ошибка запроса: код статуса {response.status_code}')
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')

        all_dates = {}
        for h3 in soup.find_all('h3'):
            date = h3.get_text()
            ul = h3.find_next_sibling('ul')
            all_dates[date] = []
            if ul:
                for li in ul.find_all('li'):
                    text = li.get_text()
                    name = li.find('a').get_text() if li.find('a') else None
                    match_age = re.search(r'\((\d{1,3})\)', text)
                    if match_age:
                        age = int(match_age.group(1))
                    if len(text.split('—')) > 1:
                        employment = text.split('—')[1]
                    if name:
                        all_dates[date].append(list((name, age, employment)))
                

    
    except:
