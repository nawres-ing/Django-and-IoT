import paho.mqtt.client as mqtt
import os
import datetime
import ssl
from rest_framework_simplejwt.tokens import AccessToken

# Initialiser Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet_examen.settings')


from django.conf import settings
from devices.models import Device
from telemetry.models import Telemetry
from alerts.models import Alert

# Callback de connexion
def on_connect(client, userdata, flags, rc):
    try:
        rc = int(rc)  # 🔧 Ajouté pour garantir que rc est bien un entier
    except Exception as e:
        print(f"Erreur de conversion de rc : {rc}, {e}")
        return
    print(f"Connecté avec le code de retour : {rc}")
    if rc == 0:
        print("Connexion réussie au broker MQTT")
        # S'abonner aux topics des appareils actifs
        devices = Device.objects.filter(is_active=True)
        for device in devices:
            print(f"Abonnement au topic : {device.topic}")
            client.subscribe(device.topic)
    else:
        print(f"Échec de connexion avec le code {rc}")

# Callback de déconnexion
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"Déconnexion inattendue avec le code {rc}")
    else:
        print("Déconnexion normale du broker MQTT")

# Callback de réception de message
def on_message(client, userdata, msg):
    print(f"Message reçu sur {msg.topic} : {msg.payload.decode()}")
    try:
        # Vérifier si l'appareil existe et est actif
        # Ajouter cette vérification après avoir récupéré l'appareil dans on_message
        try:
            device = Device.objects.get(topic=msg.topic, is_active=True)
        except Device.DoesNotExist:
            print(f"L'appareil avec le topic {msg.topic} n'existe pas ou n'est pas actif")
            return
            
            # Vérification du token si présent dans le message
            # Le token pourrait être inclus dans l'en-tête du message ou dans le payload
            # Par exemple, si le format est "token:type:valeur:unité[:valeur2]"
        parts = msg.payload.decode().strip().split(":")
        if len(parts) < 4:  # Maintenant on attend au moins 4 parties avec le token
            print("Format de message invalide ou token manquant")
            return
                
        token = parts[0]
        try:
            access_token = AccessToken(token)
        except Exception as e:
            print(f"Token JWT invalide: {e}")
            return
                
        data_type = parts[1]
        value = float(parts[2])
        unit = parts[3]
        value2 = float(parts[4]) if len(parts) >= 5 else None

        # Vérifier que le type de données est valide
        valid_data_types = [choice[0] for choice in Telemetry.DATA_TYPES]
        if data_type not in valid_data_types:
            print(f"Type de données invalide: {data_type}")
            return

        # Déterminer le statut en fonction des valeurs
        status = 'NORMAL'
        severity = None
        alert_message = None

        # Logique simple pour déterminer le statut et créer des alertes si nécessaire
        if data_type == 'HEART_RATE':
            if value < 40 or value > 150:
                status = 'CRITICAL'
                severity = 'HIGH'
                alert_message = f"Fréquence cardiaque anormale: {value} {unit}"
            elif value < 50 or value > 120:
                status = 'WARNING'
                severity = 'MEDIUM'
                alert_message = f"Fréquence cardiaque à surveiller: {value} {unit}"
        
        elif data_type == 'TEMPERATURE':
            if value < 35 or value > 40:
                status = 'CRITICAL'
                severity = 'HIGH'
                alert_message = f"Température corporelle critique: {value} {unit}"
            elif value < 36 or value > 38:
                status = 'WARNING'
                severity = 'MEDIUM'
                alert_message = f"Température corporelle à surveiller: {value} {unit}"
        
        elif data_type == 'OXYGEN':
            if value < 90:
                status = 'CRITICAL'
                severity = 'HIGH'
                alert_message = f"Niveau d'oxygène sanguin critique: {value} {unit}"
            elif value < 95:
                status = 'WARNING'
                severity = 'MEDIUM'
                alert_message = f"Niveau d'oxygène sanguin à surveiller: {value} {unit}"
        
        elif data_type == 'BLOOD_PRESSURE':
            if value > 180 or (value2 and value2 > 120):
                status = 'CRITICAL'
                severity = 'HIGH'
                alert_message = f"Tension artérielle critique: {value}/{value2} {unit}"
            elif value > 140 or (value2 and value2 > 90):
                status = 'WARNING'
                severity = 'MEDIUM'
                alert_message = f"Tension artérielle à surveiller: {value}/{value2} {unit}"

        # Créer l'entrée de télémétrie
        telemetry = Telemetry.objects.create(
            device=device,
            data_type=data_type,
            value=value,
            value2=value2,
            unite=unit,
            status=status
        )
        print(f"Télémétrie enregistrée: {telemetry}")

        # Créer une alerte si nécessaire
        if status != 'NORMAL' and severity and alert_message:
            alert = Alert.objects.create(
                device=device,
                telemetry=telemetry,
                severity=severity,
                message=alert_message,
                status='NEW'
            )
            print(f"Alerte créée: {alert}")

    except Exception as e:
        print(f"Erreur lors du traitement du message: {str(e)}")

# Fonction pour obtenir le client MQTT configuré
def get_mqtt_client():
    # Configurer le client MQTT
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect


    # Récupérer les paramètres depuis les settings
    mqtt_broker = getattr(settings, 'MQTT_BROKER_HOST', 'localhost')
    mqtt_port = int(getattr(settings, 'MQTT_BROKER_PORT', 1883))
    mqtt_keepalive = getattr(settings, 'MQTT_KEEPALIVE', 60)
    mqtt_username = getattr(settings, 'MQTT_BROKER_USERNAME', None)
    mqtt_password = getattr(settings, 'MQTT_BROKER_PASSWORD', None)
    mqtt_use_tls = getattr(settings, 'MQTT_USE_TLS', False)

    # Configurer l'authentification si nécessaire
    if mqtt_username and mqtt_password:
        client.username_pw_set(mqtt_username, mqtt_password)

    # Configurer TLS si nécessaire
    if mqtt_use_tls:
        client.tls_set(
            ca_certs=getattr(settings, 'MQTT_CA_CERTS', None),
            certfile=getattr(settings, 'MQTT_CERTFILE', None),
            keyfile=getattr(settings, 'MQTT_KEYFILE', None),
            tls_version=ssl.PROTOCOL_TLS,
        )

    # Se connecter au broker
    try:
        client.connect(mqtt_broker, mqtt_port, mqtt_keepalive)
        print(f"Tentative de connexion à {mqtt_broker}:{mqtt_port}")
    except Exception as e:
        print(f"Erreur de connexion au broker MQTT: {str(e)}")

    return client

# Cette fonction sera appelée par apps.py pour démarrer le client
def start_mqtt_client():
    client = get_mqtt_client()
    client.loop_start()  # Démarrer la boucle dans un thread séparé
    return client