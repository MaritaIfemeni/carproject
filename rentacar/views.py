from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm, CarForm, RentForm, CarImageForm, CarPickForm
from .models import CustomUser, Car, Rent, Owner

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def carimage(request):
    if request.method == 'POST':
        form = CarImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img_obj = form.instance
    
            context = {
                'form': form,
                'img_obj': img_obj,
            }

            return render(request, 'rentacar/carimage.html', context)
    else:
        form = CarImageForm()
    
        query_results = Car.objects.all()
        car_list = CarPickForm()

        cars = []

        user = request.user
        owner = Owner.objects.filter(user_id=user.userNumber)
        
        for car in owner:
            cars.append(car)

        context = {
            'query_results': query_results,
            'car_list': car_list,
            'form': form,
            'cars': cars,
        }

    return render(request, 'rentacar/carimage.html', context)

#@login_required
#def carimage(request):
#    if request.method == 'POST':
#        form = CarImageForm(request.POST, request.FILES)
#        if form.is_valid():
#            form.save()
#            img_obj = form.instance
#
#            context = {
#                'form': form,
#                'img_obj': img_obj,
#            }
#
#            return render(request, 'rentacar/carimage.html', context)
#    else:
#        form = CarImageForm()
#    return render(request, 'rentacar/carimage.html', {'form': form})

@login_required
def account(request):
    return render(request, 'rentacar/account.html')

@login_required
def carsearch(request):
    return render(request, 'rentacar/carsearch.html')

@login_required
def caradd(request):
    if request.method == "POST":
        carform = CarForm(request.POST)
        if carform.is_valid():
            car = carform.save(commit=False)
            car.save()

            owner = Owner()
            owner.assign_owner(car, request.user)
            
            return render(request, 'home.html')
    else:
        carform = CarForm()

    context = {
        'carform': carform
    }

    return render(request, 'rentacar/caradd.html', context)

@login_required
def carlist(request):
    cars = Car.objects.all()

    context = {
        'cars': cars,
    }

    return render(request, 'rentacar/carlist.html', context)

@login_required
def cardetails(request, pk):
    car = get_object_or_404(Car, pk=pk)

    context = {
        'car': car,
    }

    if (car.status == 1):
        return redirect('carnotfound')

    return render(request, 'rentacar/cardetails.html', context)

@login_required
def carnotfound(request):
    return render(request, 'rentacar/carnotfound.html')

@login_required
def carrent(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == "POST":
        rentform = RentForm(request.POST)
        if rentform.is_valid():
            rent = rentform.save(commit=False)
            rent.renterNumber_id = request.user.userNumber
            rent.carNumber_id = car.carNumber
            rent.save()
            return render(request, 'home.html')
    else:
        rentform = RentForm()

        context = {
            'rentform': rentform,
            'car': car,
        }

        return render(request, 'rentacar/carrent.html', context)