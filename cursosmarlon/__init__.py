# Importar Celery para que sea configurado cuando Django inicie
from .celery import app as celery_app

__all__ = ('celery_app',)