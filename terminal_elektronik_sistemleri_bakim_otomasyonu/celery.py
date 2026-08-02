from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'terminal_elektronik_sistemleri_bakim_otomasyonu.settings')
app = Celery('terminal_elektronik_sistemleri_bakim_otomasyonu')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()