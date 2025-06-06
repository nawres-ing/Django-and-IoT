# Django-and-IoT
Ce projet, inspiré par l'idée de notre professeur Monsieur "Bayoudhi Chaouki" , réalisé moi c'une application Django qui intègre des fonctionnalités IoT (Internet des Objets) pour la gestion de données télémétriques provenant des devices médicaux. Grâce à l'utilisation de MQTT, l'application permet la communication en temps réel entre les appareils et le serveur. Une API flexible est fournie via GraphQL pour accéder et interagir avec les données. De plus, Celery est utilisé pour démarrer un client MQTT et écouter les messages en temps réel, gérant ainsi les tâches asynchrones et assurant la réactivité de l'application

## Étapes principales et nécessaires

1.  **Configuration de l'environnement :** Assurez-vous d'avoir Docker et Docker Compose installés sur votre machine.
2.  **Configuration de Mosquitto :** Le fichier `mosquitto/mosquitto.conf` est utilisé pour configurer le broker MQTT. Il est monté en volume dans le conteneur Mosquitto.
3.  **Démarrage des services :** Utilise Docker Compose pour lancer tous les services nécessaires (Django, PostgreSQL, Redis, Mosquitto).
4.  **Initialisation de la base de données :** Applique les migrations Django et créez un superutilisateur.
5.  **Test de l'application :** Publie des messages MQTT, effectuez des requêtes GraphQL et vérifiez le fonctionnement des alertes.

## Initialisation du projet Django

mkdir projet_django_iot
cd projet_django_iot
pipenv --python 3.11
pipenv shell
django-admin startproject projet_examen
cd projet_examen
python manage.py startapp devices
python manage.py startapp telemetry
python manage.py startapp alerts
python manage.py startapp mqtt
 
## Bibliothèques installées

Django : pip install django
Graphene-Django : pip install graphene-django
Celery : pip install celery
paho-mqtt pour envoyer/recevoir des messages MQTT : pip install paho-mqtt
scikit-learn pour modele ia 'IsolationForest' : pip install scikit-learn
PostgreSQL (psycopg2) : pip install psycopg2
Redis : pip install redis
Django REST Framework (Simple JWT) : pip install djangorestframework simplejwt

## configuration de la base de données, ajout des application, graphene,rest_framework dans settings.py et creer fichier .env contient les variables d'environnement.

## Configuration de MQTT

-   **Broker MQTT :** Utilise l'image officielle de Mosquitto eclipse-mosquitto.La configuration se trouve dans le fichier docker-compose.yml

## configurartion de GraphQL

-ajouter graphene dans settings.py
-ajouter les schemas dans schema.py pour chaque model pour creer : 
     *les queries (afficher les devices , les alerts et les telemetry )
     exemple test : 
     query {
        Alldevices {
            id
            name
            description
        }
    } 
      *mutations (createAlert, createDevice, createTelemetry,sendCommandToDevice)
      exemple test :
      mutation {
          createDevice(
                name: "Capteur test",
                description: "Juste un test",
                deviceType: "TEMPERATURE",
                topic: "test/topic",
                authToken: "token123",
                isActive: true
            ) {
                device {
                id
                name
                topic
                }
            }
        }

## Configuration de Celery
  - creer un fichier tasks.py dans mqtt
  - creer un fichier celery.py dans projet_examen
      
## Configuration des services Docker

-   **Django :** Utilise l'image officielle de Django avec Python 3.11.
-   **PostgreSQL :** Utilise l'image officielle de PostgreSQL.
-   **Redis :** Utilise l'image officielle de Redis.
-   **Mosquitto :** Utilise l'image officielle de Mosquitto.
**Démarrer les services Docker :
       docker-compose up --build -d

**Appliquer les migrations Django :
    docker-compose exec web python manage.py migrate
 
**Créer un superutilisateur (administrateur) :
    docker-compose exec web python manage.py createsuperuser
**creer les fichiers docker-compose.yml et dockerfile pour la configuration.

## Accéder à l'application :

    -   Django Admin : `http://localhost:8000/admin/`
    -   GraphQL Playground : `http://localhost:8000/graphql/`
    -   API REST : `http://localhost:8000/api/`

## recuperer le token d'un device

    le token de chaque device est unique et il est généré automatiquement lors de la création d'un device.
    pour recuperer le token d'un device, il faut se connecter à l'application Django Admin et aller dans le modèle Device.
    ensuite, il faut cliquer sur le device dont on veut récupérer le token.

## tester la publication/reception des messages MQTT
    j'ai testée cette fonctionnalité en utilisant deux CMD pour publier et recevoir des messages MQTT.
    teminal 1 :
         mosquitto_sub -h localhost -p 1883 -t "patient/12/frequence_cardiaque"
    terminal 2 :
        mosquitto_pub -h localhost -p 1883 -t "patient/12/frequence_cardiaque" -m "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxODEzMjIwLCJpYXQiOjE3NDkyMjEyMjAsImp0aSI6IjYxYmZjMDU0MDQ0NjQzMDk4YzU4MTA1MWI1NWQzMzE4IiwiZGV2aWNlX2lkIjoiMTUiLCJkZXZpY2VfdG9waWMiOiJwYXRpZW50LzEyL2ZyZXF1ZW5jZV9jYXJkaWFxdWUiLCJkZXZpY2VfdHlwZSI6IkhFQVJUX1JBVEUifQ.Ts1O-fb3hz32fstO5LqtnNh55QHqEfiJXp2UP7ohUhU:HEART_RATE:160:bpm"

## Rôles des composants clés

-   **GraphQL :
 Fournit une API flexible et efficace pour interroger et manipuler les données. Il permet aux clients de demander exactement les données dont ils ont besoin, évitant une utilisation de API REST traditionnelle . Dans ce projet, il est utilisé pour interagir avec les modèles `Device`, `Telemetry` et `Alert`.
-  Celery :
 Celery est utilisé pour écouter et traiter les messages MQTT en arrière-plan, permettant de gérer des processus comme l'enregistrement des données télémétriques et la génération des alertes.

-  Docker : Conteneurise les services du projet (web, db (PostgreSQL), mqtt (Mosquitto), Redis, Celery) pour faciliter le déploiement et la gestion des environnements. Docker assure la portabilité du projet en permettant de l'exécuter dans des environnements cohérents, indépendamment du système d'exploitation.

- Mosquitto (MQTT) : Est un broker MQTT utilisé pour la communication en temps réel entre les dispositifs IoT et l'application Django. Il permet la publication et la souscription de messages, garantissant une communication fluide et rapide pour les données télémétriques.
