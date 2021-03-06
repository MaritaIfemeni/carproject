from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import DateTimeField
from django.utils import timezone

class CarImage(models.Model):
    image = models.ImageField(upload_to='images')
    car = models.ForeignKey('Car', on_delete=models.CASCADE)

    def __str__(self):
        return self.car.registerNum

    class Meta:
        db_table = "rentacar_carimage"

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

"""
class CarOwner(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
"""
class Owner(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} {self.car}"

    def assign_owner(self, car, owner):
        self.car = car
        self.user = owner
        self.save()

    def assign_new_owner(self, car, new_owner):
        self.car = car
        self.user = new_owner
        self.save()

class AddOwner(models.Model):
    owner = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    new_owner = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    car = models.ForeignKey('Car', on_delete=models.CASCADE)

    def assign_new_owner(self, car, owner, new_owner):
        self.car = car
        self.owner = owner
        self.new_owner = new_owner
        self.save()

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
    pending = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.make} {self.model}"

class Rent(models.Model):
    rentNumber = models.AutoField(primary_key=True)
    carNumber = models.ForeignKey('Car', on_delete=models.CASCADE)
    renterNumber = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name="renter")
    renteeNumber = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name="rentee")
    rentPrice = models.PositiveSmallIntegerField(default=100)
    startDate = models.DateTimeField(null=True, default=timezone.now())
    endDate = models.DateTimeField(null=True, default=timezone.now())
    expired = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.renterNumber.last_name} {self.renteeNumber.last_name} {self.carNumber.registerNum} {self.endDate}"