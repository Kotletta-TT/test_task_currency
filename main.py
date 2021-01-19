import requests
import os
import time
import db_helper

CURRENCIES = ['USD', 'EUR']
DEF_CURRENCY = 'RUB'
URL = 'http://api.openrates.io/latest?base='
DEFAULT_ROUND_TIME = 300


# Проверка корректности времени указанного в переменной окружения
def check_time(round_time):
    try:
        if 0 < int(round_time) < 86400:
            return int(round_time)
    except ValueError:
        print(f"""Время опроса указанно неверно! 
Пожалуйста передайте в переменной среды ROUND_TIME время опроса в сек. от 1 до 86400 и и перезапустите!
По умолчанию опрос происходит раз в {str(DEFAULT_ROUND_TIME)} сек\n""")
        return DEFAULT_ROUND_TIME


# Запрос к API
def get_course(curr):
    # Проверяем есть ли доступ к API
    try:
        response = requests.get(URL + curr)
        # Проверяем ответ от сервера на наличие ошибок
        if response.status_code == 200:
            return response.json()['rates'][DEF_CURRENCY]
        else:
            print(f'''Некорректный запрос! Возможно вы неверно указали валюты или одна из валют недоступна
Текст ответа: {response.json()["error"]}''')
            return False

    except ConnectionError:
        print('Нет соединения с сервисом предоставляющим API')
        return False


# Получение времени опроса API
def get_time():
    round_time = os.environ.get('ROUND_TIME')
    if round_time:
        return check_time(round_time)
    else:
        return DEFAULT_ROUND_TIME


# Сохранение в БД
def add_to_db(currency_name, value):
    session = db_helper.Session()
    row = db_helper.Currency(currency_name, value)
    session.add(row)
    session.commit()
    session.close()


def main():
    round_time = get_time()

    while True:
        for currency in CURRENCIES:
            currency_value = get_course(currency)
            if currency_value:
                add_to_db(currency, float(currency_value))

                print(' ' + currency + ' = ' + str(currency_value) + ' ' + DEF_CURRENCY)

        time.sleep(round_time)


if __name__ == '__main__':
    main()
