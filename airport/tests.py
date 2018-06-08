from datetime import timedelta, datetime

from django.utils import timezone

from django.test import TestCase

from airport.models import User, Airplane, Crew, Flight

airports = ['Lublin', 'Warszawa', 'Wroclaw', 'Opole', 'Krakow', 'Poznan', 'Szczecin', 'Gdansk', 'Radom', 'Zamosc',
            'Zakopane', 'Bialystok', 'Lodz', 'Targowek', 'Modlin']
fist_names = ['Marcin', 'Eliza', 'Anna', 'Malgorzata', 'Ewelina', 'Marek', 'Mateusz', 'Janusz', 'Blazej', 'Genowefa',
              'Bartlomiej', 'Jakub', 'Urszula', 'Waldemar', 'Pawel']
last_names = ['Kartofel', 'Urban', 'Pomidor', 'Katana', 'Pomponik', 'Guzik', 'Rondelek', 'Nicpon', 'Tenteges',
                'Bigos', 'Osiol', 'Marchewka', 'Radiator', 'Klops']

class UnitTest(TestCase):
    currentDate = timezone.now()

    def setUp(self):
        # create user
        user = User.objects.create_user(username="user", password="pass")

        # create two airplanes
        airplane1 = Airplane.objects.create(number=1, capacity=50)
        airplane2 = Airplane.objects.create(number=2, capacity=50)

        # create two crews
        crew1 = Crew.objects.create(captain_first_name=fist_names[0], captain_last_name=last_names[0])
        crew2 = Crew.objects.create(captain_first_name=fist_names[1], captain_last_name=last_names[1])


        # create two flights
        flight1 = Flight.objects.create(airplane=airplane1, crew=crew1, source="airport1", destination="airport2",
                                        departure_time=self.currentDate, arrival_time=self.currentDate + timedelta(hours=4))

        flight2 = Flight.objects.create(airplane=airplane2, crew=crew2, source="airport1", destination="airport2",
                                        departure_time=self.currentDate, arrival_time=self.currentDate + timedelta(hours=4))


    def testGetCrews(self):
        response = self.client.get('/crew/get_flight_and_crew_lists/')
        # response should be success...
        self.assertEqual(response.status_code, 200)
        # and contain both crews (yeah, I know its ugly but I have to deal with different date formats)
        string = b'{"flights": [{"pk": 1, "source": "airport1", "destination": "airport2", "departure_time": "'
        barray = list(str(self.currentDate))
        barray[10] = 'T'
        barray[23] = 'Z'
        barray = barray[:24]
        string += bytearray(''.join(barray), 'utf8')
        string += b'", "arrival_time": "'
        barray = list(str(self.currentDate + timedelta(hours=4)))
        barray[10] = 'T'
        barray[23] = 'Z'
        barray = barray[:24]
        string += bytearray(''.join(barray), 'utf8')
        string += b'"}, {"pk": 2, "source": "airport1", "destination": "airport2", "departure_time": "'
        barray = list(str(self.currentDate))
        barray[10] = 'T'
        barray[23] = 'Z'
        barray = barray[:24]
        string += bytearray(''.join(barray), 'utf8')
        string += b'", "arrival_time": "'
        barray = list(str(self.currentDate + timedelta(hours=4)))
        barray[10] = 'T'
        barray[23] = 'Z'
        barray = barray[:24]
        string += bytearray(''.join(barray), 'utf8')
        string += b'"}], "crews": [{"captain_first_name": "Marcin", "captain_last_name": "Kartofel"}, {"captain_first_name": "Eliza", "captain_last_name": "Urban"}]}'

        self.assertEqual(response.content, string)

    def testAssignCrew(self):
        # we will create new crew and replace other crew with the new one
        crew3 = Crew.objects.create(captain_first_name=fist_names[2], captain_last_name=last_names[2])

        old_crew = str(Flight.objects.get(pk=1).crew)
        response = self.client.post('/crew/assign_crew/',
                                    data={
                                        'username': 'user',
                                        'password': 'pass',
                                        'flight_pk': 1,
                                        'captain_first_name': crew3.captain_first_name,
                                        'captain_last_name': crew3.captain_last_name,
                                    })


        # response should be success...
        self.assertEqual(response.status_code, 200)
        # and we should have new crew in this flight
        new_crew = str(Flight.objects.get(pk=1).crew)
        self.assertNotEqual(old_crew, new_crew)

    def testAssignCrewFailing(self):
        # First two crews have flights in the same time, we will try to replece crew1 with cre2

        crew2 = Crew.objects.get(pk=2)
        old_crew = str(Flight.objects.get(pk=1).crew)

        response = self.client.post('/crew/assign_crew/',
                                    data={
                                        'username': 'user',
                                        'password': 'pass',
                                        'flight_pk': 1,
                                        'captain_first_name': crew2.captain_first_name,
                                        'captain_last_name': crew2.captain_last_name,
                                    })

        # response should be failure...
        self.assertEqual(response.status_code, 403)
        # and we should have the same frew in flight1
        new_crew = str(Flight.objects.get(pk=1).crew)
        self.assertEqual(old_crew, new_crew)
