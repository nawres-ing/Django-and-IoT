from celery import shared_task
import time
from .mqtt_client import get_mqtt_client

@shared_task
def mqtt_subscriber_task():
    
    #Tâche Celery pour démarrer le client MQTT et écouter les messages.
    
    print("Démarrage de la tâche Celery : MQTT listener")
    client = get_mqtt_client()
    time.sleep(3)  # Attente pour laisser le temps au serveur de se lancer complètement
    client.loop_forever()  # Boucle bloquante, mais OK dans Celery
