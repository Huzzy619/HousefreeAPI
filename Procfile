release: python manage.py makemigrations && python manage.py migrate
worker: celery -A RentRite worker -l info
web: gunicorn RentRite.asgi:application -k uvicorn.workers.UvicornWorker
