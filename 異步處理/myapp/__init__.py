# myproject/__init__.py
from __future__ import absolute_import, unicode_literals

# 啟動 Celery
from Project_1.celery import app as celery_app

__all__ = ('celery_app',)



'''

python manage.py runserver
daphne -p 9000 Project_1.asgi:application




'''
