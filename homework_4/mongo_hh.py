# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, которая будет добавлять
# только новые вакансии/продукты в вашу базу.

import json
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint


def insert_data_from_json_to_mongodb(json_filename, database_name, collection_name):
    with open(json_filename) as f:
        data = f.read()
        data_json = json.loads(data)

    client = MongoClient()
    db = client[database_name]
    hh_vacancies_collection = db[collection_name]
    for vacancy in data_json:
        hh_vacancies_collection.insert_one(vacancy)


def parse_new_hh_vacancies(position, city, pages=100):
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


def insert_new_vacancies_to_mongo_db(new_vacancies, database_name, collection_name):
    for new_vacancy in new_vacancies:
        new_link = new_vacancy['Ссылка на вакансию']
        hh_vacancies_collection = MongoClient()[database_name][collection_name]
        if not list(hh_vacancies_collection.find({'Ссылка на вакансию': new_link})):
            hh_vacancies_collection.insert_one(new_vacancy)


# # первоначальное создание базы данных с вакансиями из домашнего задания № 3
# first_insert_to_database = insert_data_from_json_to_mongodb('hh_vacancies.json', 'vacancies', 'hh_vacancies')

# добавление новых вакансий в базу
# insert_new_vacancies_to_mongo_db(parse_new_hh_vacancies('kurer', 'vladivostok'), 'vacancies', 'hh_vacancies')


# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
# (необходимо анализировать оба поля зарплаты). Для тех, кто выполнил задание с Росконтролем - напишите запрос для
# поиска продуктов с рейтингом не ниже введенного или качеством не ниже введенного (то есть цифра вводится одна, а
# запрос проверяет оба поля).

def show_salaries_higher_than_amount(salary, database_name, collection_name):
    hh_vacancies_collection = MongoClient()[database_name][collection_name]
    salaries_search = hh_vacancies_collection.find({'Зарплата от': {'$gt': salary}, 'Зарплата до': {'$gt': salary}})
    for result in salaries_search:
        pprint(result)


show_salaries_higher_than_amount(80000, 'vacancies', 'hh_vacancies')
