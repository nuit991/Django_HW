from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 設定 Django 的預設設定模組
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project_1.settings')

# 創建 Celery 應用
app = Celery('Project_1')

# 使用 Django 的設定來配置 Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自動發現任務
app.autodiscover_tasks()
