from django.contrib import admin

# Register your models here.
from detection_app import models

admin.site.register(models.Login)
admin.site.register(models.Criminaldata)