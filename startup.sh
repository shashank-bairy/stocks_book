gunicorn --bind=0.0.0.0 --timeout 600 --chdir /home/site/wwwroot stocks_book.wsgi &
celery -A stocks_book beat -l INFO &
celery -A stocks_book worker -l INFO