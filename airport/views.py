from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse

from .models import Flight, Ticket, Crew
from .models import User


def mainpage(request):
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

    return render(request, 'airport/mainpage.html', context)


def flight_details(request, flight_no):
    flight = get_object_or_404(Flight, pk=flight_no)

    departure_time_str = flight.departure_time.strftime("%Y-%m-%d %H:%M")
    arrival_time_str = flight.arrival_time.strftime("%Y-%m-%d %H:%M")

    passengers = Ticket.objects.filter(flight=flight).values('passenger')

    context = {'flight': flight, 'departure_time_str': departure_time_str, 'arrival_time_str': arrival_time_str,
               'passengers': passengers}

    return render(request, 'airport/flight_details.html', context)


@transaction.atomic
@require_POST
def login_or_register(request):
    if 'register' in request.POST:
        context = {'registration_ongoing': True}
        return render(request, 'airport/notifications.html', context)
    else:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            login_success = True
            context = {'login_success': login_success}
            return render(request, 'airport/notifications.html', context)
        else:
            login_failure = True
            context = {'login_failure': login_failure}
            return render(request, 'airport/notifications.html', context)


def registration_form(request):
    return render(request, 'airport/register.html')


def register(request):
    if 'username' not in request.POST \
            or 'password' not in request.POST \
            or 'firstname' not in request.POST \
            or 'lastname' not in request.POST:

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


@transaction.atomic
def buy_ticket(request, flight_no):
    flight = Flight.objects.filter(pk=flight_no)[0]
    if flight is None:
        context = {'no_such_flight': True}
        return render(request, 'airport/notifications.html', context)

    from django.core.exceptions import ValidationError
    try:
        ticket = Ticket.objects.create(passenger=request.user, flight=flight)
        # ticket.full_clean()
        # ticket.save()
    except ValidationError:
        passengers = Ticket.objects.filter(flight=flight).values('passenger')
        context = {'flight': flight, 'passengers': passengers, 'no_places': True}
        return render(request, 'airport/flight_details.html', context)

    passengers = Ticket.objects.filter(flight=flight).values('passenger')

    context = {'flight': flight, 'passengers': passengers, 'ticket_bought': True}
    return render(request, 'airport/flight_details.html', context)


@csrf_exempt
@require_POST
def crew_login(request):
    print("jestem w crew login")
    if 'username' not in request.POST or 'password' not in request.POST:
        print("jestem w crew login w pierwszym ifie")
        # TODO przerobic na moj typ alertu, że nie podano hasla lub loginu
        raise PermissionDenied

    who = authenticate(username=request.POST['username'], password=request.POST['password'])
    if who is None:
        print("jestem w crew login w drugim ifie ifie")
        # TODO przerobic na moj typ alertu, ze dane sie nie zgadzaja
        raise PermissionDenied

    print("jestem w crew login przed returnem")
    return HttpResponse()


def get_flight_and_crew_lists(request):
    print("jestem w get_flight_list")

    # check if this request contains day to filter or not:
    if 'day' in request.GET:
        # this request contains day to filter, check if month and year are also set
        if 'month' not in request.GET or 'year' not in request.GET:
            raise PermissionDenied

        print("jestem w get_flight_list w galezi z filtrowaniem")
        day = request.GET['day']
        month = request.GET['month']
        year = request.GET['year']
        print("requested day:", day, "requested month:", month, "requested year:", year)
        flights = list(
            Flight.objects.filter(departure_time__year=year, departure_time__month=month, departure_time__day=day)
                .values('pk', 'source', 'destination', 'departure_time', 'arrival_time'))
        crews = list(Crew.objects.values('captain_first_name', 'captain_last_name'))
        # crews = []
        # for flight in flights:
        #     if flight.crew is not None:
        #         crews.append({'captain_first_name': flight.crew.captain_first_name,
        #                       'captain_last_name': flight.crew.captain_last_name})
        # print("filtered crews:")
    else:
        # this request does not contain day to filter, so return all flights
        print("jestem w get_flight_list w galezi bez filtrowania")
        flights = list(Flight.objects.values('pk', 'source', 'destination', 'departure_time', 'arrival_time'))
        crews = list(Crew.objects.values('captain_first_name', 'captain_last_name'))

    return JsonResponse({
        'flights': flights,
        'crews': crews
    })
