# Live Post

<img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/django/django-plain-wordmark.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/sqlite/sqlite-original-wordmark.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/postgresql/postgresql-original-wordmark.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/nginx/nginx-original.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/ubuntu/ubuntu-plain-wordmark.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/vscode/vscode-original-wordmark.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/html5/html5-original-wordmark.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/css3/css3-original-wordmark.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;


**Live Post** is the social network for publishing posts, which allows users to subscribe to individual authors, add posts to the favorites, upload images. If the user forgets his password, he can request the email with the recovery code and change the password. Also realized custom authorization and caching. The backend was written in Python using Django. The frontend was written in HTML. Models, urls, views and forms were covered by tests using Unittest. Also developed [REST API](https://github.com/airatns/api_final_yatube1) for Live Post

![Yatube](https://user-images.githubusercontent.com/96816183/182358955-0a50ba2b-dc3e-434b-812f-ba7c9f5b4978.png)

## **Getting Started:**

Clone the repository:

>*git clone git@github.com:airatns/live-post.git*

Set up the virtual environment:

>*python -m venv env* \
>*source env/scripts/activate*

Install dependencies in the app using requirements.txt:

>*python -m pip install --upgrade pip* \
>*pip install -r requirements.txt*

Run migrations:

>*python manage.py migrate*

Run the app locally:

>*python manage.py runserver*

