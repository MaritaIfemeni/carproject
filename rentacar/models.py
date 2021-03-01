from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractBaseUser):
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

"""
class CarOwner(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
"""
class Owner(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)

class Car(models.Model):
    carNumber = models.AutoField(primary_key=True)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    registerNum = models.CharField(max_length=10)
    year = models.PositiveSmallIntegerField()
    powerLine = models.CharField(max_length=50)
    emissions = models.PositiveSmallIntegerField()
    seats = models.PositiveSmallIntegerField()
    location = models.CharField(max_length=50)
    status = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.make} {self.model}"

class Rent(models.Model):
    rentNumber = models.AutoField(primary_key=True)
    carNumber = models.ForeignKey('Car', on_delete=models.CASCADE)
    renterNumber = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name="renter")
    renteeNumber = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name="rentee")
    rentPrice = models.PositiveSmallIntegerField(default=100)
    startDate = models.DateTimeField(null=True)
    endDate = models.DateTimeField(null=True)
    expired = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.rentNumber} {self.renterNumber.last_name} {self.renteeNumber.last_name} {self.endDate}"