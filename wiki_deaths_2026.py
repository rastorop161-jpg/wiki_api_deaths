import requests
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
            date = h3.get_text().strip()
            ul = h3.find_next('ul')
            all_dates[date] = []
            if ul:
                for li in ul.find_all('li'):
                    text = li.get_text().strip()
                    name = li.find('a').get_text().strip() if li.find('a') else None
                    match_age = re.search(r'\((\d{1,3})\)', text)
                    if match_age:
                        age = int(match_age.group(1))
                    else:
                        age = None
                    if len(text.split('—')) > 1:
                        employment = text.split('—')[1]
                    else:
                        employment = None
                    if name:
                        all_dates[date].append((name, age, employment))

        if not all_dates:
            print('Не найдено записей.')
            return

        def age(x):
            return x[1]
        while True:
            date_request = input('Укажите дату в формате "число месяц" (например, "10 июня"): ').strip()
            if date_request not in all_dates:
                print('Ошибка ввода. Повторите попытку.')
                continue
            if not all_dates[date_request]:
                print('Нет записей за эту дату.')
                continue
            else:
                print(f'Самый молодой умерший - {min(all_dates[date_request], key = age)[0]}, возраст - {min(all_dates[date_request], key = age)[1]}, род занятий - {min(all_dates[date_request], key = age)[2]} \n'
                f'Самый старый умерший - {max(all_dates[date_request], key = age)[0]}, возраст - {max(all_dates[date_request], key = age)[1]}, род занятий - {max(all_dates[date_request], key = age)[2]}')
                break

        input('Нажмите ввод для выхода...')
                
    except Exception as e:
        print(f'Ошибка {e}.')


main()