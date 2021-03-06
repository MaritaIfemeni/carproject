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

class CarAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
         {'fields': ['carNumber', 'make', 'model', 'registerNum', 'year', 'powerLine', 'emissions', 'seats', 'location',
         'status', 'pending', 'main_owner']}),
    ]

    readonly_fields = ('carNumber',)
    list_display = ('carNumber', 'make', 'model', 'registerNum', 'year', 'powerLine', 'emissions', 'seats', 'location',
                    'status', 'pending', 'main_owner')    
    list_filter = ['main_owner']

class RentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
        {'fields': ['rentNumber', 'carNumber', 'renterNumber', 'renteeNumber', 'rentPrice', 'startDate', 'endDate', 'expired']}),
    ]

    readonly_fields = ('rentNumber',)
    list_display = ('rentNumber', 'carNumber', 'renterNumber', 'renteeNumber', 'rentPrice', 'startDate', 'endDate', 'expired')
    list_filter = ('renterNumber', 'renteeNumber')

class OwnerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
        {'fields': ['car', 'user']}),
    ]

    readonly_fields = ('id',)
    list_display = ('id', 'car', 'user')
    list_filter = ('car',)

admin.site.register(Car, CarAdmin)
admin.site.register(Rent, RentAdmin)
admin.site.register(Owner, OwnerAdmin)