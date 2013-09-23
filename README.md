nextfeed
========

A minimalistic RSS reader


Development Guide
=================

1. Get a copy of the repository
```bash
git clone https://github.com/Nurdok/nextfeed
```

2. Create a virtual Python environment
```bash
cd nextfeed
virtualenv venv
```

3. Install the required dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

4. Create a development database;
```bash
python manage.py syncdb
```

When asked whether to create a superuser, create one. Its details aren't 
important and are local to your machine.

4. Develop:  
You can run a test server in one of two ways:
```bash
python manage.py runserver
```
or
```bash
honcho start
```
The difference is that `honcho` also runs a scheduler and worker, which are
Celery processes that poll feeds for changes. These are probably not important
in a development machine unless you're testing a polling-specific feature.



