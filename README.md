[![Build Status](https://github.com/GA10v/graduate_work/actions/workflows/checks.yml/badge.svg?branch=main)](https://github.com/GA10v/graduate_work/actions/workflows/checks.yml)

# Проектная работа: диплом

У вас будет один репозиторий на все 4 недели работы над дипломным проектом.

Если вы выбрали работу в командах, ревью будет организовано как в командных модулях с той лишь разницей, что формируете состав команды и назначаете тимлида вы сами, а не команда сопровождения.

Удачи!

## dev

1. Установить зависимости командой
   `$ poetry install`
2. Установить pre-commit командой
   `$ pre-commit install`
3. Создать внешнюю сеть "project-network" командой:
   `$ docker network create 'project-network'`

## Запуск ELK

1. Создать внешнюю сеть "project-network" командой:
   `$ docker network create 'project-network'`
2. Зпустить контейнер командой
   `$ cd ELK && docker-compose up`

## Запуск локально

1. Установить зависимости командой
   `$ poetry install`
2. Создать файл конфигурации `.env` в корне проекта и заполнить его согласно `example.env`
3. Запустить API командой:
   `$ python3 backend/Booking/booking_api/src/main.py`
4. Запустить Watcher командой:
   `$ python3 backend/Booking/watcher/src/main.py`
5. Полученить access_jwt_token командой:
   `$ python3 jwt_token.py`
6. Перейти к документации API по url: `http://localhost:8080/api/openapi`

## Запуск в docker

1. Создать файл конфигурации `.env` в корне проекта и заполнить его согласно `example.env`
2. Создать внешнюю сеть "project-network" командой:
   `$ docker network create 'project-network'`
3. Запустить контейнер командой
   `$ docker-compose up`
4. Полученить access_jwt_token командой:
   `$ python3 jwt_token.py`
5. Перейти к документации API по url: `http://localhost:8080/api/openapi`
6. Перейти к документации Mock_Auth по url: `http://localhost:8081/api/openapi`
7. Перейти к документации Mock_Admin_panel по url: `http://localhost:8082/api/openapi`
8. Перейти к документации Mock_ugc по url: `http://localhost:8083/api/openapi`

### Запуск тестов

1. Создать файл конфигурации `.env` в корне проекта и заполнить его согласно `example.env`
2. Запустить контейнер командой
   `$ docker-compose -f docker-compose.test.yml up`
