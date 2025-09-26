import os
from celery import Celery

# Configurar el módulo de configuración de Django para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cursosmarlon.settings')

app = Celery('cursosmarlon')

# Usar string para que el worker no tenga que importar el objeto de configuración
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodescubrir tareas de todas las aplicaciones instaladas
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')