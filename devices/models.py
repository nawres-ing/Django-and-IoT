from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from rest_framework_simplejwt.tokens import RefreshToken


# Create your models here.
class Device(models.Model):
    DEVICE_TYPES = [
        ('HEART_RATE', 'Capteur de fréquence cardiaque'),
        ('BLOOD_PRESSURE', 'Capteur de tension artérielle'),
        ('TEMPERATURE', 'Capteur de température corporelle'),
        ('OXYGEN', 'Capteur d\'oxygène sanguin'),
    ]
    name = models.CharField(max_length=255,verbose_name="Nom du capteur")
    description = models.TextField(blank=True,verbose_name="Description")
    device_type = models.CharField(max_length=100,choices=DEVICE_TYPES,verbose_name="Type de capteur")

    topic = models.CharField(max_length=255, unique=True,verbose_name="Adresse MQTT")
    auth_token = models.CharField(max_length=512, unique=True, null=True, blank=True,verbose_name="Token d'authentification MQTT")

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True,verbose_name="Capteur actif")

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.name} ({self.get_device_type_display()})"
    
    def generate_device_token(self):
        
        token = RefreshToken()
        token['device_id'] = str(self.id)
        token['device_topic'] = self.topic
        token['device_type'] = self.device_type

        self.auth_token = str(token.access_token)
        self.save(update_fields=['auth_token'], generating_token=True)  # évite la boucle
        return self.auth_token

    #pour appeler automatiquement la fonction generate_device_token lors de creation d'un Device
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        # Ajouter un flag pour éviter la récursion
        generating_token = kwargs.pop('generating_token', False)
        
        super().save(*args, **kwargs)
    
        if is_new and not self.auth_token and not generating_token:
            self.generate_device_token()
            