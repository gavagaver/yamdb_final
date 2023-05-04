# Проект YaMDb
[![CI](https://github.com/gavagaver/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?branch=master)](https://github.com/gavagaver/yamdb_final/actions/workflows/yamdb_workflow.yml)

REST API проект для сервиса YaMDb — сбор отзывов о фильмах, книгах или музыке.
## Описание

Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: Книги, Фильмы, Музыка.

Список категорий (Category) может быть расширен (например, можно добавить категорию Изобразительное искусство или Ювелирка).

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории Книги могут быть произведения Винни Пух и все-все-все и Марсианские хроники, а в категории Музыка — песня Давеча группы Насекомые и вторая сюита Баха.

Произведению может быть присвоен жанр из списка предустановленных (например, Сказка, Рок или Артхаус). Новые жанры может создавать только администратор.

Благодарные или возмущённые читатели оставляют к произведениям текстовые отзывы (Review) и выставляют произведению рейтинг (оценку в диапазоне от одного до десяти). Из множества оценок автоматически высчитывается средняя оценка произведения.

## Шаблон файла .env
### Файл необходимо разместить по пути ```infra/.env```
```sh
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
DB_HOST=db
DB_PORT=5432
SECRET_KEY=p&l%385148ksll%385148ksll%385148ksll%385148ksl
```


## Установка и запуск

1. [x] Клонируем репозиторий 
```bash
 git clone git@github.com:gavagaver/infra_sp2.git 
```
1. [x] Создаем и запускаем докер-контейнеры
``` 
docker-compose up -d --build 
```
1. [ ] Создаем миграции
``` 
docker-compose exec web python manage.py makemigrations 
```
1. [ ] Применяем миграции
``` 
docker-compose exec web python manage.py migrate 
``` 
1. [ ] Создаем суперпользователя
``` 
docker-compose exec web python manage.py createsuperuser 
``` 
1. [ ] Собираем статику
``` 
docker-compose exec web python manage.py collectstatic --no-input 
``` 
1. [ ] Заполняем базу данными
``` 
docker-compose exec web python manage.py loaddata <путь до файла>
``` 


Проект доступен по [ссылке](http://158.160.68.180)
