from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Car, Rent

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['userNumber', 'username', 'first_name', 'last_name', 'email',
                    'phoneNum', 'address', 'postcode', 'city', 'country', 'paymentMethod',]

# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Car)
admin.site.register(Rent)
