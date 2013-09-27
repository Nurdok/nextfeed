from .base import *

# Celery
BROKER_URL = 'amqp://fecnwrea:A9Rx3kA6tGwia4f5qCxptN6hSIASQYjy@bunny.cloudamqp.com/fecnwrea'
BROKER_POOL_LIMIT = 1

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] = dj_database_url.config()
