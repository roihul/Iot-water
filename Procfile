release: python manage.py install
web: gunicorn --worker-class eventlet -w 1 socketio_web:app --preload
worker: celery -A celery_worker.celery worker --loglevel=INFO