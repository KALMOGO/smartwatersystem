from django.contrib import admin
from .models import *
# Register your models here.

# Register your models here.
admin.site.register([UserPerson, UserIoT,waterParameters, WaterParameterPred, WaterQualityPred])