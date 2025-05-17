from __future__ import absolute_import, unicode_literals

import os

import django
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tradelink.settings")
django.setup()

app = Celery("tradelink")
app.conf.enable_utc = False
app.conf.update(timezone="Africa/Lagos")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
