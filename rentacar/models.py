from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    userNumber = models.AutoField(primary_key=True)
    email = models.CharField(max_length=50)
    phoneNum = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    postcode = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    paymentMethod = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Car(models.Model):
    # with open('populate_db/brandslist.txt', 'r') as f:
        # brandchoice = f.read()

    brandchoice = [('ferrari', 'Ferrari'), ('lamborghini', 'Lamborghini'),]

    carNumber = models.AutoField(primary_key=True)
    make = models.CharField(choices=brandchoice, max_length=1)
    model = models.CharField(max_length=50)
    registerNum = models.CharField(max_length=10)
    year = models.PositiveSmallIntegerField()
    powerLine = models.CharField(max_length=50)
    emissions = models.PositiveSmallIntegerField()
    seats = models.PositiveSmallIntegerField()
    location = models.CharField(max_length=50)
    status = models.PositiveSmallIntegerField(default=0)
    carOwner = models.ForeignKey('CustomUser', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.make} {self.model}"
