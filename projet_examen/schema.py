import graphene
import devices.schema
import telemetry.schema
import alerts.schema

#contient toutes les requêtes pour lire (consulter) des données (lecture seule) dans API GraphQL
class Query(
    devices.schema.Query,
    telemetry.schema.Query,
    alerts.schema.Query,graphene.ObjectType):
    pass

#contient toutes les opérations d’écriture/modification que je veux exposer via GraphQL (comme : créer un capteur, supprimer une alerte, modifier une télémétrie).
#regroupe toutes les mutations (create, update, delete) de toutes mes apps (les modifications)
class Mutation(      
    devices.schema.Mutation,
    telemetry.schema.Mutation,
    alerts.schema.Mutation,
    graphene.ObjectType):
    pass    

schema = graphene.Schema(query=Query, mutation=Mutation) #le point d’entrée principal de l’API GraphQL 
#je peux accéder à tout le système GraphQL à partir de /graphql/