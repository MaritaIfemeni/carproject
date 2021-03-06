from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from django.db.models import Q
from django.utils import timezone

from .forms import CustomUserCreationForm, CarForm, CarImageForm, RentForm
from .models import CustomUser, Car, Rent, Owner, AddOwner

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
        imageform = CarImageForm(request.POST, request.FILES)
        imageform.base_fields['car'].queryset = Car.objects.all()
        if imageform.is_valid():
            imageform.save()
            img_obj = imageform.instance
    
            context = {
                'imageform': imageform,
                'img_obj': img_obj,
                'selected_car': selected_car,
                'owner': owner,
            }

            return render(request, 'rentacar/carimage.html', context)
    else:
        imageform = CarImageForm()
        imageform.base_fields['car'].queryset = Car.objects.all()
        context = {
            'imageform': imageform,
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

def coownership(request, pk):
    car = Car.objects.get(pk=pk)
    car_owner = AddOwner.objects.filter(car=car)
    new_owner = car_owner.latest('requestDate')

    if request.user != new_owner.owner:
        return render(request, '/')

    owner = Owner()
    owner.assign_owner(car, new_owner.new_owner)

    car.pending = False
    car.save()

    context = {
        'car': car,
    }

    return render(request, 'rentacar/coownership.html', context)

@login_required
def account(request):
    pending_cars = Owner.objects.filter(user=request.user).filter(car__pending=1)
    pending_cars_new = AddOwner.objects.filter(owner=request.user)
    pending_cars_new_owner = pending_cars_new.latest('requestDate')
    pending_cars_count = pending_cars.count()

    context = {
        'pending_cars': pending_cars,
        'pending_cars_count': pending_cars_count,
        'pending_cars_new_owner': pending_cars_new_owner,
    }

    return render(request, 'rentacar/account.html', context)

@login_required
def cars(request):
    my_cars = Owner.objects.filter(user=request.user)

    context = {
        'my_cars': my_cars,
    }

    return render(request, 'rentacar/cars.html', context)

@login_required
def rents(request):
    rents = Rent.objects.filter(renterNumber_id=request.user.userNumber)
    val_rents = rents.filter(expired=0).filter(carNumber__status=1)
    exp_rents = rents.filter(expired=1)
    val_rents_count = val_rents.count()
    exp_rents_count = exp_rents.count()

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
        'exp_rents_count':exp_rents_count,
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
    expired_rentsout_count =expired_rentsout.count()

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
        'expired_rentsout_count' : expired_rentsout_count,
    }

    return render(request, 'rentacar/rentsout.html', context)

@login_required
def carsearch(request):
    text = None
    cars = None
    if 'search' in request.POST:
        regsearch = request.POST.get('searchfield')
        cars = Car.objects.filter(registerNum__icontains=regsearch)

    if 'request' in request.POST:
        selected_car = request.POST.get('sel_car')
        sel_car = Car.objects.get(carNumber=selected_car)
        owner = Owner.objects.filter(car__carNumber=sel_car.carNumber).first()

        new_owner = AddOwner()
        new_owner.assign_new_owner(sel_car, owner.user, request.user)

        sel_car.pending = True
        sel_car.save()

        text = "Your request is now pending..."
            
    context = {
        'cars': cars,
        'text': text,
    }

    return render(request, 'rentacar/carsearch.html', context)

@login_required
def caradd(request):
    if request.method == "POST":
        carform = CarForm(request.POST, initial={'main_owner': request.user})
        if carform.is_valid():
            car = carform.save(commit=False)
            car.save()

            owner = Owner()
            owner.assign_owner(car, request.user)
            
            return redirect('cars')

    else:
        carform = CarForm()

    context = {
        'carform': carform
    }

    return render(request, 'rentacar/caradd.html', context)

@login_required
def carlist(request):
    searched = None

    if request.method == "POST":
        makesearch = request.POST.get('makesearch')
        seatsearch = request.POST.get('seatsearch')
        locationsearch = request.POST.get('locationsearch')

        if makesearch != '' and seatsearch != '' and locationsearch != '':
            searched = Car.objects.filter(make__icontains=makesearch).filter(seats=seatsearch).filter(location__icontains=locationsearch)
        elif makesearch != '' and seatsearch != '':
            searched = Car.objects.filter(make__icontains=makesearch).filter(seats=seatsearch)
        elif makesearch != '' and locationsearch != '':
            searched = Car.objects.filter(make__icontains=makesearch).filter(location__icontains=locationsearch)
        elif seatsearch != '' and locationsearch != '':
            searched = Car.objects.filter(seats=seatsearch).filter(location__icontains=locationsearch)  
        elif makesearch != '':
            searched = Car.objects.filter(make__icontains=makesearch)
        elif seatsearch != '':
            searched = Car.objects.filter(seats=seatsearch)
        elif locationsearch != '':
            searched = Car.objects.filter(location=locationsearch)

    # filtered_cars = []
    # cars = Car.objects.all()
    # uniq_cars = Owner.objects.values_list('car_id', flat=True).distinct()
    # filt_uniq_cars = uniq_cars.filter(~Q(user_id=user_number))
    # for i in range(len(filt_uniq_cars)):
    #     for j in range(len(cars)):
    #         if filt_uniq_cars[i] == cars[j].carNumber:
    #             filtered_cars.append(cars[j])
    
    # user_number = request.user.userNumber
    # cars = Owner.objects.filter(car__status=0).filter(~Q(user_id=user_number))
    # rented_cars = Rent.objects.filter(carNumber__status=1).filter(~Q(renterNumber_id=user_number))

    cars = Car.objects.filter(status=0)
    rented_cars = Rent.objects.filter(~Q(carNumber__status=0))

    context = {
        'cars': cars,
        'rented_cars': rented_cars,
        'searched': searched,
    }

    return render(request, 'rentacar/carlist.html', context)

@login_required
def cardetails(request, pk):
    teksti = None
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        teksti = "Lähetä sähköpostia osoitteeseen blabla"

        context = {
            'teksti': teksti,
            'car': car,
        }

        return render(request, 'rentacar/cardetails.html', context)

    context = {
        'car': car,
    }

    return render(request, 'rentacar/cardetails.html', context)

@login_required
def carnotfound(request):
    return render(request, 'rentacar/carnotfound.html')

@login_required
def carrent(request, pk):
    car = get_object_or_404(Car, pk=pk)

    if car.status != 0:
            return redirect('carnotfound')

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

        context = {
            'rentform': rentform,
            'car': car,
            'owners': owners,
        }

        return render(request, 'rentacar/carrent.html', context)