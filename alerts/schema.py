import graphene
from graphene_django import DjangoObjectType
from.models import Alert
from datetime import datetime

class AlertType(DjangoObjectType):
    class Meta:
        model = Alert

class Query(graphene.ObjectType):
    all_alerts = graphene.List(AlertType)

    def resolve_all_alerts(self, info):
        return Alert.objects.select_related('device','telemetry').all()

class CreateAlert(graphene.Mutation):
    class Arguments:
        device_id = graphene.ID(required=True)
        telemetry_id = graphene.ID(required=True)
        severity = graphene.String(required=True)
        message = graphene.String(required=True)

    alert = graphene.Field(AlertType)

    def mutate(self, info, device_id, telemetry_id, severity, message):
        alert = Alert(device_id=device_id, telemetry_id=telemetry_id, severity=severity, message=message)
        alert.save()
        return CreateAlert(alert=alert)

class ResolveAlert(graphene.Mutation):
    class Arguments:
        alert_id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, alert_id):
        alert = Alert.objects.get(pk=alert_id)
        alert.status = 'RESOLVED'
        alert.resolve_date= datetime.now()
        alert.save()
        return ResolveAlert(success=True)

class Mutation(graphene.ObjectType):
    create_alert = CreateAlert.Field()
    resolve_alert = ResolveAlert.Field()
