from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from datetime import datetime

from django.views.decorators.http import require_POST

from .models import Flight
from django.db.models import Q


def mainpage(request):
    if request.GET.get('search'):
        search = datetime.strptime(request.GET['search'], '%Y-%m-%d')
        flights = Flight.objects.filter(Q(startTime__day=search.day, startTime__month=search.month) |
                                        Q(endTime__day=search.day, endTime__month=search.month)).order_by('startTime')
    else:
        flights = Flight.objects.all().order_by('departure_time')

    template = loader.get_template('airport/mainpage.html')
    context = {'flights_list': flights}
    return HttpResponse(template.render(context, request))


def flight_details(request, flight_no):
    flight = get_object_or_404(Flight, pk=flight_no)

    # TODO get passengers and tickets

    template = loader.get_template('airport/flight_details.html')
    context = {'flight': flight}
    return HttpResponse(template.render(context, request))

@transaction.atomic
@require_POST
def login_or_register(request):
    # TODO maybe I should create django form?
    # chyba mozna tez sprawdzac request.POST['register']='on'?
    # TODO zrobic zeby to bylo w okienku
    if 'register' in request.POST:
        print("uzytkownik chce sie zarejestrowac")
        if User.objects.all().filter(username=request.POST['email']).exists():
            print("uzytkownik juz istnieje - blad")
            register_failure = True
            context = {'register_failure' : register_failure}
            return render(request, 'airport/account.html', context)
        else:
            print("uzytkownik nie istnieje - tworze nowe konto")
            register_success = True
            user = User.objects.create_user(
                username=request.POST['email'], password=request.POST['password'])
            login(request, user)
            context = {'register_success' : register_success}
            return render(request, 'airport/account.html', context)
    else:
        print("uzytkownik chce sie zalogowac")
        user = authenticate(username=request.POST['email'], password=request.POST['password'])
        if user is not None:
            print("uzytkownik istnieje")
            login(request, user)
            login_success = True
            context = {'login_success': login_success}
            return render(request, 'airport/account.html', context)
        else:
            print("uzytkownik nie istnieje")
            login_failure = False
            context = {'login_failure': login_failure}
            return render(request, 'airport/account.html', context)

def logout_view(request):
    logout(request)
    logout_success = True
    context = {'logout_success': logout_success}
    return render(request, 'airport/account.html', context)

