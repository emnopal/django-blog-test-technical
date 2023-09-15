# Django Blog

before run server: copy `.env.example` then rename it to `.env`

run django server: `docker-compose up -d`

post docker run:

`docker-compose run blog_web python manage.py makemigrations`

`docker-compose run blog_web python manage.py migrate`
