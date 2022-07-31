# Yatube

Проект Yatube - это социальная сеть для публикации постов. С авторизацией, персональными лентами, комментариями, с возможностями добавления картинок и подписки на авторов.

## **Стек технологий**

Python, Django, SQL, Gunicorn, Nginx, PostgreSQL, Яндекс.Облако(Ubuntu)

## **Как запустить проект:**

Клонировать репозиторий и перейти в него в командной строке:

>*git clone https://github.com/airatns/api_final_yatube.git*

Cоздать и активировать виртуальное окружение:

>*python3 -m venv env*

>*source env/scripts/activate*

Установить зависимости из файла requirements.txt:

>*python3 -m pip install --upgrade pip*

>*pip install -r requirements.txt*

Выполнить миграции:

>*python3 manage.py migrate*

Запустить проект:

>*python3 manage.py runserver*

