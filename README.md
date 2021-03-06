# » nextfeed

[![Build Status](https://travis-ci.org/Nurdok/nextfeed.png?branch=master)](https://travis-ci.org/Nurdok/nextfeed)
[![Coverage Status](https://coveralls.io/repos/Nurdok/nextfeed/badge.png?branch=master)](https://coveralls.io/r/Nurdok/nextfeed?branch=master)

*nextfeed* is a minimalistic RSS reader.
With *nextfeed*, you define a list of feeds you want to follow, and get a 
personalized URL. Every time you hit that URL, you'll get the next unread 
entry in your feeds.


## Development Guide

### Work on Issues

If you want to contribute to `nextfeed`, you're welcome!  
Either pick an existing issue or create a new one and state that you are
working on it (to make sure nobody else is working on the same issue). If you 
are in a "collaborator" status, simply assign the issue to yourself. 
Otherwise, post a comment saying you're working on it.

### Create a Development Environment

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
pip install -r nextfeed/requirements/local.txt
```

4. Create a development database*: 
```bash
python manage.py syncdb --settings=nextfeed.settings.local
```
When asked whether to create a superuser, create one. Its details aren't 
important and are local to your machine.

4. Develop:  
You can run a test server in one of two ways*:  
```bash
python manage.py runserver --settings=nextfeed.settings.local
```
or  
```bash
honcho start
```
The difference is that `honcho` also runs a scheduler and worker, which are
Celery processes that poll feeds for changes. These are probably not important
in a development machine unless you're testing a polling-specific feature.

*If you want to avoid using `--settings=nextfeed.settings.local`, you can 
just set the environment variable `DJANGO_SETTINGS_MODULE` to the same value.




