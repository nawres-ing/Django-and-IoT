import graphene
from graphene_django import DjangoObjectType
from .models import Telemetry

class TelemetryType(DjangoObjectType):
    class Meta:
        model = Telemetry

class Query(graphene.ObjectType):
    all_telemetry = graphene.List(TelemetryType)

    def resolve_all_telemetry(self, info):
        return Telemetry.objects.select_related('device').all()

class CreateTelemetry(graphene.Mutation):
    telemetry = graphene.Field(TelemetryType)

    class Arguments:
        device_id = graphene.ID(required=True)
        status=graphene.String(required=True,default_value='NORMAL')
        data_type=graphene.String(required=True)
        value=graphene.Float(required=True)
        value2=graphene.Float(required=True)
        unite=graphene.String(required=True)

    def mutate(self, info, device_id, status, data_type, value, value2, unite):
        telemetry = Telemetry(device_id=device_id, status=status, data_type=data_type, value=value, value2=value2, unite=unite)
        telemetry.save()
        return CreateTelemetry(telemetry=telemetry)

class Mutation(graphene.ObjectType):
    create_telemetry = CreateTelemetry.Field()