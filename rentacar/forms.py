from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField
from django.db import router
from django.forms.fields import DateTimeField
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

        startDate = forms.DateField(
        widget=forms.DateInput(format='%m/%d/%Y'),
        input_formats=('%m/%d/%Y', )
        )

        endDate = forms.DateField(
        widget=forms.DateInput(format='%m/%d/%Y'),
        input_formats=('%m/%d/%Y', )
        )

class CarImageForm(forms.ModelForm):
    class Meta:
        model = CarImage
        fields = ('image',)
