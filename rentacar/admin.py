from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Car, Rent, Owner

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['userNumber', 'username', 'first_name', 'last_name', 'email',
                    'phoneNum', 'address', 'postcode', 'city', 'country', 'paymentMethod',]

# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Rent)
admin.site.register(Owner)

class CarAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
         {'fields': ['carNumber', 'make', 'model', 'registerNum', 'year', 'powerLine', 'emissions', 'seats', 'location',
         'status', 'pending', 'main_owner']}),
    ]

    readonly_fields = ('carNumber', 'make', 'model', 'registerNum', 'year', 'powerLine', 'emissions', 'seats', 'location')
    list_display = ('carNumber', 'make', 'model', 'registerNum', 'year', 'powerLine', 'emissions', 'seats', 'location',
                    'status', 'pending', 'main_owner')    
    list_filter = ['main_owner']

admin.site.register(Car, CarAdmin)