from typing import Iterable
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from rest_framework_api_key.models import APIKey
from .qualityDetection import *

User = get_user_model()

class UserIoT(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True
    )
    located_at  = models.CharField(max_length=250)
    longitude   = models.CharField(max_length=250, blank=True, null=True)
    latitude    = models.CharField(max_length=250, blank=True, null=True)
    water_name  = models.CharField(max_length=250)
    zone_id     = models.SlugField(max_length=255, blank=True, null=True)
    api_key     = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        ordering = ["located_at"]

    def __str__(self):
        return self.water_name
    
    def save(self, *args, **kwargs):
        if not self.api_key:
            _, key = APIKey.objects.create_key(name=self.user.first_name)
            self.api_key = key
        super().save(*args, **kwargs)

class UserPerson(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True
    )
    created_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

class waterParameters(models.Model):
    ph          = models.CharField(max_length=250, blank=True, null=True)
    oxygen      = models.CharField(max_length=250, blank=True, null=True)
    turbidity   = models.CharField(max_length=250, blank=True, null=True)
    temperature = models.CharField(max_length=250, blank=True, null=True)
    created_at  = models.DateField(auto_now=True)
    harvesting_time = models.DateTimeField(auto_now=True)
    site = models.CharField(max_length=250, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-harvesting_time"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        quality = mainQualityDetection(self.temperature) # Prediction de la qualité de l'eau à chaque  ajout
        WaterQualityPred.objects.create(parameter=self, quality=quality)
        self.quality = quality
        
    @property
    def get_quality(self):
        return self.quality
    
    def __str__(self) -> str:
        return f"Temp:{self.temperature} PH:{self.ph} Oxygen:{self.oxygen} Turb:{self.turbidity} user:{self.user.first_name} {self.harvesting_time}"

class WaterQualityPred(models.Model):
    created_at = models.DateField(auto_now=True)
    parameter  = models.ForeignKey(waterParameters, on_delete=models.CASCADE)
    quality    = models.BooleanField(default=False)
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self) -> str:
        return f"Temp:{self.parameter.temperature} PH:{self.parameter.ph} Oxygen:{self.parameter.oxygen} Turb:{self.parameter.turbidity} ===> quality : {self.quality} "


class WaterParameterPred(models.Model):
    lower_border = models.DateTimeField()
    data_source = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateField(auto_now=True)
    upper_border = models.DateTimeField()
    parameter = models.CharField(max_length=250, blank=True, null=True)
    user = models.ForeignKey(UserPerson, on_delete=models.CASCADE)
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self) -> str:
        return f"{self.parameter} source: {self.data_source}"
    