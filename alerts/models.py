from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator,MinLengthValidator
from devices.models import Device
from telemetry.models import Telemetry

# Create your models here.
class Alert(models.Model):
    SEVERITY_LEVELS=[
        ('LOW','Faible'),
        ('MEDIUM','Moyenne'),
        ('HIGH','Elevée'),
        ('CRITICAL', 'Critique'),
    ]
    STATUS_CHOICES =[
        ('NEW','Nouvelle'),
        ('RESOLVED','Resolue'),
    ]

    device = models.ForeignKey(Device,on_delete=models.CASCADE,related_name='alerts')
    telemetry=models.ForeignKey(Telemetry,on_delete=models.CASCADE,related_name='alerts')
    severity = models.CharField(max_length=20,choices=SEVERITY_LEVELS,default='LOW',verbose_name="Niveau de gravité")
    message = models.TextField(validators=[MinLengthValidator(5)], verbose_name="Message d'alerte")
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='NEW',verbose_name="Statut")
    timestamp = models.DateTimeField(auto_now_add=True,verbose_name="Date de mesure")
    resolve_date = models.DateTimeField(null=True,blank=True,verbose_name="Date de résolution")
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.device.name} - {self.get_severity_display()} - {self.status} - {self.timestamp}"