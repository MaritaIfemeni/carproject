import django
django.setup()

import random
from rentacar.models import Car
from django.contrib.auth import get_user_model

alphabet = ["a","b","c","d","e","f","g","e","h","i","j","k","l",
            "m","n","o","p","q","r","s","t","y","v","w","x","y","z"]

powerLines = ["Gasoline", "Diesel", "Hybrid", "Electric"]

User = get_user_model()
owners = User.objects.all()

with open("populate_db/brands.txt", "r") as f:
    content = f.read()

brands = content.split(',')

with open("populate_db/kunnat.txt", "r") as f:
    locations_content = f.read()

locations = locations_content.split(',')

for i in range(10):
    vmake = brands[random.randint(0,len(brands)-1)]
    with open(f"populate_db/{vmake}.txt", "r") as f:
        model_content = f.read()

    models = model_content.split(',')
    vmodel = models[random.randint(0,len(models)-1)]
    print(f"{vmake} {vmodel}")

    vregisterNum = ""

    for i in range(3):
        let = alphabet[random.randint(0,len(alphabet)-1)]
        vregisterNum += let

    vregisterNum += f"-{random.randint(1,999)}"

    vlocation = locations[random.randint(0,len(locations)-1)]

    Car.objects.bulk_create([
        Car(make=vmake, model=vmodel, registerNum=vregisterNum, year=random.randint(1990,2020),
            powerLine=powerLines[random.randint(0,3)], emissions=random.randint(100,300), 
            seats=random.randint(2,7), location=vlocation, carOwner=owners[0]),
    ])
