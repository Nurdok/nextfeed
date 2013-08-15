web: gunicorn nextfeed.wsgi
scheduler: python project/manage.py celeryd -B -E --settings=nextfeed.settings
worker: python project/manage.py celeryd -E --settings=nextfeed.settings
