from .models import Car, CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()
owner = User.objects.filter(username='mintai')

Car.objects.bulk_create([
    Car(make='ferrari', model='testarossa', registerNum='XXX-111', year=1984,
        powerLine='Gasoline', emissions=300, seats=2, location='Italy', carOwner=owner)
])