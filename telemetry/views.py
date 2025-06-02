from rest_framework import viewsets
from .models import Telemetry
from .serializers import TelemetrySerializer

class TelemetryViewSet(viewsets.ModelViewSet):
    queryset = Telemetry.objects.all()
    serializer_class = TelemetrySerializer

# Create your views here.
