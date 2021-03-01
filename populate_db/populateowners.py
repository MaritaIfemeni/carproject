import django
django.setup()

from rentacar.models import CustomUser, Car, Owner

users = CustomUser.objects.all()
cars = Car.objects.all()

for i in range(len(users)):

    vcar = users[i]
    vuser = cars[i]

    Owner.objects.bulk_create([
        Owner(car=vcar, user=vuser)
    ])