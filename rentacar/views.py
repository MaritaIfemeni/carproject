from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from django.db.models import Q
from django.utils import timezone

from .forms import CustomUserCreationForm, CarForm, CarImageForm, RentForm
from .models import CustomUser, Car, Rent, Owner

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

"""
# Doesn't work...
@login_required
def carimage(request):
    car = Car.objects.filter(carNumber=1)
    user = CustomUser.objects.filter(userNumber=1)
    if request.method == 'POST':
        form = CarImageForm(request.POST, request.FILES)
        if form.is_valid():
            selected_car = request.POST.get('idsel_car')
            # form.save()

            context = {
                'form': form,
                'car': car,
                'selected_car': selected_car,
                'user': user,
            }

            return render(request, 'rentacar/carimage.html', context)
    else:
        form = CarImageForm()

        context = {
            'form': form,
            'car': car,
            'user': user,
        }

        return render(request, 'rentacar/carimage.html', context)
"""

# TOTALLY FUCKED!
@login_required
def carimage(request):
    user = request.user
    owner = Owner.objects.filter(user_id=user.userNumber)
    if request.method == 'POST':
        form = CarImageForm(request.POST, request.FILES)
        if form.is_valid():
            selected_car = request.POST.get("idsel_car")
            form.car = Car.objects.filter(carNumber=selected_car)
            # form.save()
            img_obj = form.instance
    
            context = {
                'form': form,
                'img_obj': img_obj,
                'selected_car': selected_car,
                'owner': owner,
            }

            return render(request, 'rentacar/carimage.html', context)
    else:
        form = CarImageForm()

        context = {
            'form': form,
            'owner': owner,
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

def help(request):
    return render(request, 'rentacar/help.html')

@login_required
def account(request):
    return render(request, 'rentacar/account.html')

@login_required
def cars(request):
    return render(request, 'rentacar/cars.html')

@login_required
def rents(request):
    rents = Rent.objects.filter(renterNumber_id=request.user.userNumber)
    val_rents = rents.filter(expired=0).filter(carNumber__status=1)
    exp_rents = rents.filter(expired=1)
    val_rents_count = val_rents.count()

    carchoice = []

    if request.method == 'POST':
        carchoice = request.POST.getlist('carchoice')
        for i in range(len(carchoice)):
            car = Car.objects.get(carNumber=carchoice[i])
            car.status = 2
            car.save()

            rent = Rent.objects.get(carNumber_id=carchoice[i], expired=0)
            rent.endDate = timezone.now()
            rent.expired = 1
            rent.save()

    context = {
        'val_rents': val_rents,
        'val_rents_count': val_rents_count,
        'exp_rents': exp_rents,
        'carchoice': carchoice,
    }

    return render(request, 'rentacar/rents.html', context)

@login_required
def rentsout(request):
    rentsout = Rent.objects.filter(renteeNumber_id=request.user.userNumber)
    valid_rentsout = rentsout.filter(expired=0).filter(carNumber__status=1)
    returned_rentsout = rentsout.filter(carNumber__status=2)
    expired_rentsout = rentsout.filter(expired=1)
    valid_rentsout_count = valid_rentsout.count()

    returncarchoice = []

    if request.method == 'POST':
        returncarchoice = request.POST.getlist('returncarchoice')
        for i in range(len(returncarchoice)):
            car = Car.objects.get(carNumber=returncarchoice[i])
            car.status = 0
            car.save()

    context = {
        'valid_rentsout': valid_rentsout,
        'valid_rentsout_count': valid_rentsout_count,
        'returned_rentsout': returned_rentsout,
        'expired_rentsout': expired_rentsout,
    }

    return render(request, 'rentacar/rentsout.html', context)

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
    makesearch = ""
    if request.method == "POST":
        makesearch = request.POST.get('makesearch')

    user_number = request.user.userNumber
    
    # filtered_cars = []
    # cars = Car.objects.all()
    # uniq_cars = Owner.objects.values_list('car_id', flat=True).distinct()
    # filt_uniq_cars = uniq_cars.filter(~Q(user_id=user_number))
    # for i in range(len(filt_uniq_cars)):
    #     for j in range(len(cars)):
    #         if filt_uniq_cars[i] == cars[j].carNumber:
    #             filtered_cars.append(cars[j])
    
    cars = Owner.objects.filter(car__status=0).filter(~Q(user_id=user_number))
    rented_cars = Rent.objects.filter(carNumber__status=1).filter(~Q(renterNumber_id=user_number))

    context = {
        'cars': cars,
        'rented_cars': rented_cars,
        'makesearch': makesearch,
    }

    return render(request, 'rentacar/carlist.html', context)

@login_required
def cardetails(request, pk):
    car = get_object_or_404(Car, pk=pk)

    context = {
        'car': car,
    }

    if (car.status != 0):
        return redirect('carnotfound')

    return render(request, 'rentacar/cardetails.html', context)

@login_required
def carnotfound(request):
    return render(request, 'rentacar/carnotfound.html')

@login_required
def carrent(request, pk):
    car = get_object_or_404(Car, pk=pk)
    owners = Owner.objects.filter(car_id=car.carNumber)
    if request.method == "POST":
        rentform = RentForm(request.POST)
        if rentform.is_valid():
            rent = rentform.save(commit=False)
            rent.renterNumber_id = request.user.userNumber
            rent.renteeNumber_id = owners.first().user.userNumber
            rent.carNumber_id = car.carNumber
            rent.save()

            car.status = 1
            car.save()

            return redirect('rents')
    else:
        rentform = RentForm()

        # if car.status

        context = {
            'rentform': rentform,
            'car': car,
            'owners': owners,
        }

        return render(request, 'rentacar/carrent.html', context)