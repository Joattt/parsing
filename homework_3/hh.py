import requests
from bs4 import BeautifulSoup as bs
import json
import pandas as pd


def parse_hh_vacancies(position, city, pages):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }

    total_vacancies_list = []
    for page in range(pages):
        address = f'https://{city}.hh.ru/vacancies/{position}?page={page}'
        response = requests.get(address, headers=headers)
        soup = bs(response.content, 'html.parser')
        vacancies = soup.find_all('a', attrs={'class': ['serp-item__title']})
        if not vacancies:
            break

        vacancies_list = []
        for vacancy in vacancies:
            title = vacancy.text
            link = vacancy['href']
            salary = vacancy.parent.parent.find_next_sibling('span')
            if salary:
                salary_list = salary.text.split()
                if salary_list[0].isdigit():
                    min_salary = int(salary_list[0] + salary_list[1])
                    max_salary = int(salary_list[3] + salary_list[4])
                    currency = salary_list[-1]
                elif salary_list[0] == 'от':
                    min_salary = int(salary_list[1] + salary_list[2])
                    max_salary = 'не указано'
                    currency = salary_list[-1]
                elif salary_list[0] == 'до':
                    min_salary = 'не указано'
                    max_salary = int(salary_list[1] + salary_list[2])
                    currency = salary_list[-1]
            else:
                min_salary = 'не указано'
                max_salary = 'не указано'
                currency = 'не указано'

            vacancies_dict = {
                'Наименование вакансии': title,
                'Зарплата от': min_salary,
                'Зарплата до': max_salary,
                'Валюта': currency,
                'Ссылка на вакансию': link,
                'Сайт': 'HeadHunter'
            }
            vacancies_list.append(vacancies_dict)
        total_vacancies_list += vacancies_list
    return total_vacancies_list


data = parse_hh_vacancies('kurer', 'vladivostok', 5)

with open('hh_vacancies.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)

df = pd.DataFrame(data=data)
pd.set_option('display.max_colwidth', None)
pd.options.display.expand_frame_repr = False
print(df)
