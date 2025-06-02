from django.db import models
from django.conf import settings
from devices.models import Device
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

# Create your models here.
class Telemetry(models.Model):
    DATA_TYPES = [
        ('HEART_RATE', 'Fréquence cardiaque'),
        ('BLOOD_PRESSURE', 'Tension artérielle'),
        ('TEMPERATURE', 'Température corporelle'),
        ('OXYGEN', 'Oxygène sanguin'),
    ]

    STATUS_CHOICES = [
        ('NORMAL', 'Normale'),
        ('WARNING', 'Avertissement'),
        ('CRITICAL', 'Critique'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NORMAL')

    data_type = models.CharField(max_length=100,choices=DATA_TYPES,verbose_name="Type de données")

    value = models.FloatField(verbose_name="Valeur")
    value2 = models.FloatField(null=True,blank=True,verbose_name="Valeur secondaire") #pour la tension artérielle (Diastolique et Systolique) 
    unite=models.CharField(max_length=10,verbose_name="Unité de mesure")
    
    timestamp = models.DateTimeField(auto_now_add=True,verbose_name="Date de mesure")
    received_at=models.DateTimeField(auto_now=True,verbose_name="Date de réception")

    device=models.ForeignKey(Device,on_delete=models.CASCADE,related_name='telemetry_data')

    class Meta:
        ordering = ['-timestamp']
        constraints =[
            models.CheckConstraint(
                check=models.Q(timestamp__lte=models.F('received_at')),name='timestamp_before_received_at'
            )
        ]

    def __str__(self):
        return f"{self.device.name} - {self.get_data_type_display()} - {self.value} - {self.timestamp}"