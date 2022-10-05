# Yatube

<img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/django/django-plain-wordmark.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/mysql/mysql-original-wordmark.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/sqlite/sqlite-original-wordmark.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/postgresql/postgresql-original-wordmark.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/nginx/nginx-original.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/ubuntu/ubuntu-plain-wordmark.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/vscode/vscode-original-wordmark.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;

Проект Yatube - это социальная сеть для публикации постов. С авторизацией, персональными лентами, комментариями, с возможностями добавления картинок и подписки на авторов. Регистрация реализована с верификацией данных, есть возможность смены и восстановления пароля через почту. Использованы пагинация постов и кеширование. Написаны тесты, проверяющие работу сервиса. Проект запущен на сервере в Яндекс.Облако

![Yatube](https://user-images.githubusercontent.com/96816183/182358955-0a50ba2b-dc3e-434b-812f-ba7c9f5b4978.png)

## **Как запустить проект:**

Клонировать репозиторий и перейти в него в командной строке:

>*git clone git@github.com:airatns/hw05_final_yatube.git*

Cоздать и активировать виртуальное окружение:

>*python -m venv env* \
>*source env/scripts/activate*

Установить зависимости из файла requirements.txt:

>*python -m pip install --upgrade pip* \
>*pip install -r requirements.txt*

Выполнить миграции:

>*python manage.py migrate*

Запустить проект:

>*python manage.py runserver*

