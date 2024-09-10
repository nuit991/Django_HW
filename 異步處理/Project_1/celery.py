
#absolute_import: 确保导入模块时使用绝对导入而不是相对导入。这有助于避免模块导入冲突，特别是在有复杂包结构的项目中。
#unicode_literals: 在 Python 2.x 中，使得所有字符串文字被解释为 Unicode 字符串（在 Python 3.x 中默认行为）。
from __future__ import absolute_import, unicode_literals
import os
#从 Celery 包中导入 Celery 类。Celery 是一个异步任务队列/作业队列系统，允许你在后台运行耗时的任务或定时任务。
from celery import Celery

# 这行代码的目的是告诉 Django 应用程序应该加载 Project_1 项目的 settings.py 配置文件。它是 Django 启动时的关键步骤，确保项目运行时能加载正确的设置。
# 這一段告诉 Django 去加载这些配置，使得 Django 知道如何启动项目、连接数据库、加载应用、处理静态文件等。
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project_1.settings')

#创建一个 Celery 实例。'Project_1' 是这个 Celery 应用的名字。通常，Celery 应用的名称与项目名称一致，以便于管理和调试。
app = Celery('Project_1')

# 从 Django 设置中加载 Celery 配置。namespace='CELERY' 表示 Celery 配置项应以 CELERY_ 前缀作为前缀。
# 例如，CELERY_BROKER_URL 会从 Django 的设置中读取。这样，你可以在 Django 的 settings.py 中配置 Celery 的相关参数。
app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery 会遍历所有已注册的 Django 应用，并自动发现每个应用中的任务模块（通常是 tasks.py 文件）
# 这样，你可以将任务定义在不同的 Django 应用中，Celery 会自动加载这些任务。
app.autodiscover_tasks()


'''
pip install celery
這東西用在__init__.py裡面


这段代码完成了以下任务：
Celery 是一个用于处理异步任务的任务队列库。它允许你将任务分配给后台工作进程，从而使这些任务在主程序的前台流程中异步执行。
这种方式特别适用于需要长时间处理或频繁执行的任务，如发送电子邮件、处理图像或执行复杂计算等。

设置 Django 的环境配置，使 Celery 能够访问 Django 的设置。
创建一个 Celery 实例，配置其使用 Django 的设置来配置 Celery。
自动发现和注册所有应用中的任务，使 Celery 可以处理这些任务。

'''