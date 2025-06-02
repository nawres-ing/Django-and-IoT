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

        # Importer ici pour éviter les imports circulaires
        from .mqtt_client import start_mqtt_client

        # Démarrer le client MQTT dans un thread séparé
        def start_client():
            # Attendre un peu pour s'assurer que Django est complètement démarré
            time.sleep(5)
            self.mqtt_client = start_mqtt_client()

        thread = threading.Thread(target=start_client)
        thread.daemon = True  # Le thread s'arrêtera quand le programme principal s'arrête
        thread.start()
