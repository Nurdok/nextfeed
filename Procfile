web: gunicorn nextfeed.wsgi
scheduler: python manage.py celery worker -B -E --settings=nextfeed.settings.production
worker: python manage.py celery worker -E --settings=nextfeed.settings.production
