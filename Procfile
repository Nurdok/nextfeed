web: gunicorn nextfeed.wsgi
scheduler: python manage.py celeryd -B -E --settings=nextfeed.settings
worker: python manage.py celeryd -E --settings=nextfeed.settings
