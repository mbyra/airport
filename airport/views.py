from .models import User
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from datetime import datetime, timedelta

from django.views.decorators.http import require_POST

from .models import Flight, Ticket
from django.db.models import Q


def mainpage(request):
    template = loader.get_template('airport/mainpage.html')

    if 'searchfrom' not in request.GET:
        flights = Flight.objects.all()
        context = {'flights_list': flights.order_by('departure_time')}
    else:
        searchfrom = datetime.strptime(request.GET['searchfrom'], '%Y-%m-%d')
        flights = Flight.objects.filter(Q(departure_time__gte=searchfrom))
        searchto = datetime.strptime(request.GET['searchto'], '%Y-%m-%d')
        flights = flights.filter(Q(departure_time__lte=(searchto)))
        context = {'flights_list': flights.order_by('departure_time'), 'searchfrom': request.GET['searchfrom'],
                   'searchto': request.GET['searchto']}


    return HttpResponse(template.render(context, request))


def flight_details(request, flight_no):
    flight = get_object_or_404(Flight, pk=flight_no)

    departure_time_str = flight.departure_time.strftime("%Y-%m-%d %H:%M")
    arrival_time_str = flight.arrival_time.strftime("%Y-%m-%d %H:%M")

    tickets = Ticket.objects.filter(flight=flight)
    passengers = []
    for ticket in tickets:
        passengers.append(str(ticket.passenger))

    template = loader.get_template('airport/flight_details.html')
    context = {'flight': flight, 'departure_time_str': departure_time_str, 'arrival_time_str': arrival_time_str,
               'passengers': passengers}
    return HttpResponse(template.render(context, request))


@transaction.atomic
@require_POST
def login_or_register(request):
    if 'register' in request.POST:
        print("uzytkownik chce sie zarejestrowac")
        context = {'registration_ongoing': True}
        return render(request, 'airport/notifications.html', context)
    else:
        print("uzytkownik chce sie zalogowac")
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            print("uzytkownik istnieje")
            login(request, user)
            login_success = True
            context = {'login_success': login_success}
            return render(request, 'airport/notifications.html', context)
        else:
            print("uzytkownik nie istnieje")
            login_failure = True
            context = {'login_failure': login_failure}
            return render(request, 'airport/notifications.html', context)


def registration_form(request):
    return render(request, 'airport/register.html')


def register(request):
    print("uzytkownik chce sie zarejestrowac")
    if 'username' not in request.POST \
            or 'password' not in request.POST \
            or 'firstname' not in request.POST \
            or 'lastname' not in request.POST:

        print("Blad w danych POST:")
        if 'username' not in request.POST:
            print('username not in post')
        if 'password' not in request.POST:
            print('password not in post')
        if 'firstname' not in request.POST:
            print('firstname not in post')
        if 'lastname' not in request.POST:
            print('lastname not in post')

        context = {'registration_post_data_error': True}
        return render(request, 'airport/notifications.html', context)

    elif User.objects.all().filter(username=request.POST['username']).exists():
        context = {'registration_user_exists': True}
        return render(request, 'airport/notifications.html', context)

    else:
        user = User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password'],
            first_name=request.POST['firstname'],
            last_name=request.POST['lastname']
        )
        login(request, user)
        context = {'registration_success': True, }
        return render(request, 'airport/notifications.html', context)


def logout_view(request):
    logout(request)
    context = {'logout_success': True}
    return render(request, 'airport/notifications.html', context)


def buy_ticket(request, flight_no):
    flight = Flight.objects.filter(pk=flight_no)[0]
    if flight is None:
        context = {'no_such_flight': True}
        return render(request, 'airport/notifications.html', context)

    tickets = Ticket.objects.filter(flight=flight)

    from django.core.exceptions import ValidationError
    try:
        Ticket.objects.create(passenger=request.user, flight=flight)
    except ValidationError:
        passengers = []
        for ticket in tickets:
            passengers.append(str(ticket.passenger))
        context = {'flight': flight, 'passengers': passengers, 'no_places': True}
        return render(request, 'airport/flight_details.html', context)

    passengers = []
    for ticket in tickets:
        passengers.append(str(ticket.passenger))
    context = {'flight': flight, 'passengers': passengers, 'ticket_bought': True}
    return render(request, 'airport/flight_details.html', context)
