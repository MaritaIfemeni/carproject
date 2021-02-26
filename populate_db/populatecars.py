import random
import os
# from rentacar.models import Car
# from django.contrib.auth import get_user_model

# User = get_user_model()
# owners = User.objects.all()

print(os.listdir())

with open("brands.txt", "r") as f:
    content = f.read()

brands = content.split(',')

for i in range(100):
    make = brands[random.randint(0,len(brands))]
    with open(f"{make}.txt", "r") as f:
        model_content = f.read()
    models = content.split(',')
    model = models[random.randint(0,len(models))]
    print(f"{make} {model}")

# Car.objects.bulk_create([
#     Car(make='ferrari', model='testarossa', registerNum='XXX-111', year=1984,
#         powerLine='Gasoline', emissions=300, seats=2, location='Italy', carOwner=owner),
# ])