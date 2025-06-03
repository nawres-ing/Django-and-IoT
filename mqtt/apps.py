from django.apps import AppConfig
import threading
import time


class MqttConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mqtt'
    mqtt_client = None

    def ready(self):
        # Éviter de démarrer le client MQTT lors des appels à manage.py
        import sys
        if 'runserver' not in sys.argv:
            return

        from .tasks import mqtt_subscriber_task
        mqtt_subscriber_task.delay()
