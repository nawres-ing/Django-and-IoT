# Django-and-IoT
Ce projet est une application Django qui intègre des fonctionnalités IoT (Internet des Objets) pour la gestion de données télémétriques provenant de dispositifs médicaux. Il utilise MQTT pour la communication en temps réel, GraphQL pour une API flexible, et Celery pour la gestion des tâches asynchrones.

## Étapes principales et nécessaires

1.  **Configuration de l'environnement :** Assurez-vous d'avoir Docker et Docker Compose installés sur votre machine.
2.  **Configuration de Mosquitto :** Le fichier `mosquitto/mosquitto.conf` est utilisé pour configurer le broker MQTT. Il est monté en volume dans le conteneur Mosquitto.
3.  **Démarrage des services :** Utilisez Docker Compose pour lancer tous les services nécessaires (Django, PostgreSQL, Redis, Mosquitto).
4.  **Initialisation de la base de données :** Appliquez les migrations Django et créez un superutilisateur.
5.  **Test de l'application :** Publiez des messages MQTT, effectuez des requêtes GraphQL et vérifiez le fonctionnement des alertes.

## Commandes d'installation et de démarrage

mkdir projet_django_iot
cd projet_django_iot
pipenv --python 3.11
pipenv shell
pipenv install django
pipenv install djangorestframework graphene-django celery paho-mqtt scikit-learn
pipenv install psycopg2
pip install djangorestframework-simplejwt (pour tokens)


  **Cloner le dépôt :**
    ```bash
    git clone <URL_DU_DEPOT>
    cd projet_django_iot/projet_examen
    ```
**Démarrer les services Docker :**
    ```bash
    docker-compose up --build -d
    ```
**Appliquer les migrations Django :**
    ```bash
    docker-compose exec web python manage.py migrate
    ```
**Créer un superutilisateur (administrateur) :**
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```
**Accéder à l'application :**
    -   Django Admin : `http://localhost:8000/admin/`
    -   GraphQL Playground : `http://localhost:8000/graphql/`

## Rôles des composants clés

-   **GraphQL :** Fournit une API flexible et efficace pour interroger et manipuler les données. Il permet aux clients de demander exactement les données dont ils ont besoin, évitant ainsi le sur-fetch ou le sous-fetch de données. Dans ce projet, il est utilisé pour interagir avec les modèles `Device`, `Telemetry` et `Alert`.
-   **Celery :** Un système de file d'attente de tâches distribuées. Il est utilisé pour gérer les tâches asynchrones et planifiées, comme le traitement des messages MQTT entrants en arrière-plan, afin de ne pas bloquer le thread principal de l'application Django.
