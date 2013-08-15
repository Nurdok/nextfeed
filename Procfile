web: gunicorn nextfeed.wsgi
scheduler: python manage.py worker -B -E --settings=nextfeed.settings
worker: python manage.py worker -E --settings=nextfeed.settings
