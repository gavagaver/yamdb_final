# Проект YaMDb - сервис отзывов

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

1. [ ] Клонируем репозиторий 
```bash
 git clone git@github.com:gavagaver/yamdb_final.git 
```
1. [ ] Выполняем вход на удаленный сервер
2. [ ] Устанавливаем на сервере docker
```bash
apt install docker.io 
```
1. [ ] Устанавливаем на сервере docker-compose
```bash
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```
1. [ ] Создаем и запускаем docker-контейнеры
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
## Стек
- Python 3.7
- Django 3.2
- Django REST Framework
- PostgreSQL
- gunicorn
- nginx
- Яндекс.Облако (Ubuntu 20.04)
- Simple-JWT
- GIT

## Авторы

[gavagaver](https://github.com/gavagaver)

[Antisyslik](https://github.com/Antisyslik) 

[grinfeldV](https://github.com/grinfeldV)
