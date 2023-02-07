release: python manage.py migrate
web: gunicorn RentRite.asgi:application -k uvicorn.workers.UvicornWorker
worker: celery -A RentRite worker --loglevel=INFO