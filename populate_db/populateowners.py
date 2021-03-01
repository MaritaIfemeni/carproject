import django
django.setup()

from rentacar.models import CustomUser, Car, Owner

from django.contrib.auth.models import User

users = CustomUser.objects.all()
cars = Car.objects.all()

for i in range(len(users)):

    vcar = users[i]
    vuser = cars[i]

    Owner.objects.bulk_create([
        Owner(car=vcar, user=vuser)
    ])