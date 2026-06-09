import requests
from datetime import datetime
import re

def main():
    year = '2026'
    url = f'https://ru.wikipedia.org/wiki/Список_умерших_в_{year}_году'
    headers = {'User-Agent': 'wiki_deaths_bot/1.0 (Rastorop161, rastorop161@gmail.com, https://github.com/rastorop161-jpg) study_project'}
   
    try:
        response = requests.get(url, headers = headers, timeout = 30)
        if response.status_code != 200:
            print(f'Ошибка запроса: код статуса {response.status_code}')
            return
        


    
    except:
