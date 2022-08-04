# Yatube

Проект Yatube (<a href="https://airatsakhib.hopto.org" target="_blank">Website</a>)- это социальная сеть для публикации постов. С авторизацией, персональными лентами, комментариями, с возможностями добавления картинок и подписки на авторов. Регистрация реализована с верификацией данных, есть возможность смены и восстановления пароля через почту. Использованы пагинация постов и кеширование. Написаны тесты, проверяющие работу сервиса. Проект запущен на сервере в Яндекс.Облако

![Yatube](https://user-images.githubusercontent.com/96816183/182358955-0a50ba2b-dc3e-434b-812f-ba7c9f5b4978.png)

## **Стек технологий**

Python, Django, SQL, Gunicorn, Nginx, PostgreSQL, Яндекс.Облако(Ubuntu)

## **Как запустить проект:**

Клонировать репозиторий и перейти в него в командной строке:

>*git clone git@github.com:airatns/hw05_final_yatube.git*

Зайти в папку с проектом. Cоздать и активировать виртуальное окружение:

>*python -m venv env*

>*source env/scripts/activate*

Установить зависимости из файла requirements.txt:

>*python3 -m pip install --upgrade pip*

>*pip install -r requirements.txt*

Выполнить миграции:

>*python3 manage.py migrate*

Запустить проект:

>*python3 manage.py runserver*

