from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Login(AbstractUser):
    is_state = models.BooleanField(default=False)
    is_police = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    name = models.CharField(max_length=25, null=True)
    contact_no = models.CharField(max_length=10, null=True)
    district = models.CharField(max_length=25,null=True)
    designation = models.CharField(max_length=25,null=True)
    station = models.CharField(max_length=25,null=True)


class Criminaldata(models.Model):
    name = models.CharField(max_length=25)
    age = models.IntegerField()
    crime = models.CharField(max_length=25)
    place = models.CharField(max_length=25)
    crime_status = models.CharField(max_length=25)
    photo = models.ImageField(upload_to='criminal_data')

    def __str__(self):
        return self.name


class Missingdata(models.Model):
    name = models.CharField(max_length=25)
    case = models.CharField(max_length=25)
    gender = models.CharField(max_length=25)
    age = models.IntegerField()
    date = models.DateField()
    photo = models.ImageField(upload_to='missing_data')
