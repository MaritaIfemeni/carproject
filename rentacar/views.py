from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.db.models import Q

from .forms import CustomUserCreationForm, CarForm
from .models import CustomUser, Car

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def caradd(request):
    if request.method == "POST":
        carform = CarForm(request.POST)
        if carform.is_valid():
            car = carform.save(commit=False)
            car.carOwner = request.user
            car.save()
            return render(request, 'home.html')
    else:
        carform = CarForm()

    context = {
        'carform': carform
    }

    return render(request, 'rentacar/caradd.html', context)

def carlist(request):
    cars = Car.objects.filter(status=0).filter(~Q(carOwner=request.user))

    context = {
        'cars': cars,
    }

    return render(request, 'rentacar/carlist.html', context)