from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Car, Rent, CarImage, Owner

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email',
                 'phoneNum', 'address', 'postcode', 'city', 'country')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email',
                 'phoneNum', 'address', 'postcode', 'city', 'country')

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('make', 'model', 'registerNum', 'year', 'powerLine',
        'emissions', 'seats', 'location')

class RentForm(forms.ModelForm):
    class Meta:
        model = Rent
        fields = ('startDate', 'endDate')

class CarImageForm(forms.ModelForm):
    class Meta:
        model = CarImage
        fields = ('image', 'car',)

    def __init__(self, user, *args, **kwargs):
        super(CarImageForm, self).__init__(*args, **kwargs)
        owner = Owner.objects.filter(user=user)
        self.fields['car'].queryset = Car.objects.all()