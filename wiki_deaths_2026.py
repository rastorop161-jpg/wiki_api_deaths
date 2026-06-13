import requests
import re
from bs4 import BeautifulSoup

def main():

    try:

        def get_age(x):
            return x[1] if x[1] is not None else -1
        while True:
            choiсe = input(f'Выберите опцию, введя соответствующую цифру:\n' 
            f'1. Вывести информацию о самом молодом, самом старом умершем за выбранный день.\n'
            f'2. Завершить работу программы.\n')
        
            if choiсe == '1':

                when_str_user = input(f'Введите информацию о месяце, годе, к которому относится запрашиваемая информация в формате "мае_2026_года".')
                url = f'https://ru.wikipedia.org/wiki/Умершие_в_{when_str_user}'
                headers = {'User-Agent': 'wiki_deaths_bot/1.0 (Rastorop161, rastorop161@gmail.com, https://github.com/rastorop161-jpg) study_project'}
            
                response = requests.get(url, headers = headers, timeout = 30)

                if response.status_code != 200:
                    print(f'Ошибка запроса: код статуса {response.status_code}')
                    return
            
                soup = BeautifulSoup(response.text, 'html.parser')

                all_dates = {}
                for h2 in soup.find_all('h2'):
                    date = h2.get_text().strip()
                    ul = h2.find_next('ul')
                    all_dates[date] = []
                    if ul:
                        for li in ul.find_all('li'):
                            text = li.get_text().strip()
                            name = li.find('a').get_text().strip() if li.find('a') else None
                            match_age = re.search(r'\((\d{1,3})\)', text)
                            if match_age:
                                person_age = int(match_age.group(1))
                            else:
                                person_age = None
                            if len(text.split('—')) > 1:
                                employment = text.split('—')[1]
                            else:
                                employment = None
                            if name:
                                all_dates[date].append((name, person_age, employment))

                if not all_dates:
                    print('Не найдено записей.')
                    return

                while True:
                    date_request = input('Укажите дату в формате "число месяц" (например, "10 июня") или введите "назад": ').strip()
                    if date_request == 'назад':
                        break
                    if date_request not in all_dates:
                        print('Ошибка ввода. Повторите попытку.')
                        continue
                    if not all_dates[date_request]:
                        print('Нет записей за эту дату.')
                        continue
                    else:
                        print(f'Самый молодой умерший - {min(all_dates[date_request], key = get_age)[0]}, возраст - {min(all_dates[date_request], key = get_age)[1]}, род занятий - {min(all_dates[date_request], key = get_age)[2]} \n'
                        f'Самый старый умерший - {max(all_dates[date_request], key = get_age)[0]}, возраст - {max(all_dates[date_request], key = get_age)[1]}, род занятий - {max(all_dates[date_request], key = get_age)[2]}')
                    
            if choiсe == '2':
                break

                
    except Exception as e:
        print(f'Ошибка {e}.')


main()