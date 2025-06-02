import graphene
from graphene_django import DjangoObjectType #Cela transforme ton modèle Django Device en un type GraphQL utilisable dans une requête, avec tous les champs du modèle disponibles dans l’API GraphQL.
from .models import Device

class DeviceType(DjangoObjectType): #Cela transforme ton modèle Django Device en un type GraphQL utilisable dans une requête, avec tous les champs du modèle disponibles dans l’API GraphQL.
    class Meta:
        model = Device

class Query(graphene.ObjectType): #Elle contient les requêtes disponibles dans GraphQL.
    all_devices = graphene.List(DeviceType)

    def resolve_all_devices(self, info): #C’est la fonction qui va exécuter réellement la requête. Elle est appelée automatiquement quand tu fais une requête allDevices
        return Device.objects.all()

#pour creer une mutation pour ajouter un device
class CreateDevice(graphene.Mutation):
    device = graphene.Field(DeviceType)

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        device_type=graphene.String(required=True)
        topic=graphene.String(required=True)
        auth_token=graphene.String(required=True)
        is_active=graphene.Boolean(required=True)

    def mutate(self, info, name, description, device_type, topic, auth_token, is_active):
        device = Device(name=name, description=description , device_type=device_type, topic=topic, auth_token=auth_token, is_active=is_active)
        device.save()
        return CreateDevice(device=device)

class SendCommandToDevice(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()
    device=graphene.Field(DeviceType)

    class Arguments:
        device_id = graphene.ID(required=True)
        command = graphene.String(required=True)

    def mutate(self, info, device_id, command):
        device = Device.objects.get(id=device_id)
        if device:
            device.send_command(command)
            return SendCommandToDevice(success=True, message="Commande envoyée avec succès", device=device)
        else:
            return SendCommandToDevice(success=False, message="Capteur non trouvé")

class Mutation(graphene.ObjectType):
    create_device = CreateDevice.Field()
    send_command_to_device = SendCommandToDevice.Field()