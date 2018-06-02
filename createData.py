# run with: python manage.py shell < createData.py

from datetime import timedelta
from random import randint, choice

from django.utils import timezone

from airport.models import User, Flight, Airplane, Ticket

airports = ['Lublin', 'Warszawa', 'Wroclaw', 'Opole', 'Krakow', 'Poznan', 'Szczecin', 'Gdansk', 'Radom', 'Zamosc',
            'Zakopane', 'Bialystok', 'Lodz', 'Targowek', 'Modlin']
fist_names = ['Marcin', 'Eliza', 'Anna', 'Malgorzata', 'Ewelina', 'Marek', 'Mateusz', 'Janusz', 'Blazej', 'Genowefa',
              'Bartlomiej', 'Jakub', 'Urszula', 'Waldemar', 'Pawel']
last_names = ['Kartofel', 'Urban', 'Pomidor', 'Katana', 'Pomponik', 'Guzik', 'Rondelek', 'Nicpon', 'Tenteges',
                'Bigos', 'Osiol', 'Marchewka', 'Radiator', 'Klops']

# Create airplanes:
for i in range(50):
    airplane_number = 1000 + i
    airplane_capacity = 20 + randint(0, 100)
    Airplane.objects.create(number=airplane_number, capacity=airplane_capacity)

print("Airplanes created")

# Create users:
counter = 1
for i in range(len(fist_names)):
    for j in range(len(last_names)):
        user = User.objects.create_user(username="user" + str(counter), password="user" + str(counter))
        user.first_name = fist_names[i]
        user.last_name = last_names[j]
        user.save()
        counter += 1

print("Users created")

# Create flights
for i in range(60):
    airplane = choice(Airplane.objects.all())
    source = choice(airports)
    airports.remove(source)
    destination = choice(airports)
    airports.append(source)
    departure_time = timezone.now() + timedelta(hours=randint(1, 20), minutes=randint(0,59))
    arrival_time = departure_time + + timedelta(minutes=30) + timedelta(hours=randint(1, 20), minutes=randint(0,59))
    Flight.objects.create(airplane=airplane, source=source, destination=destination, departure_time=departure_time, arrival_time=arrival_time)

print("Flights created")

# Make every passenger buy 2 random tickets
for passenger in User.objects.all():
    flight = choice(Flight.objects.all())

    from django.core.exceptions import ValidationError
    try:
        Ticket.objects.create(passenger=passenger, flight=flight)
    except ValidationError:
        pass # airplane is full

    flight = choice(Flight.objects.all())

    from django.core.exceptions import ValidationError
    try:
        Ticket.objects.create(passenger=passenger, flight=flight)
    except ValidationError:
        pass # airplane is full

print("Tickets created")