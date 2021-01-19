## Test task Get_Currency_and_save

Данный сервис собирает из открытых источников с помощью API инофрмацию (USD/RUB, EUR/RUB) и хранит их в БД.

Для задания периода опроса необходимо в Dockerfile изменить ENV ROUND_TIME=10 на свое число в секундах.

Сборка:

`docker build -t curency-app .` - в папке с проектом

Запуск:

`docker run -it --rm -v <path to folder storage data>:/usr/src/app/db_currency --name exchange-currency currency-app`