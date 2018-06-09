from datetime import timedelta

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from airport.models import User, Airplane, Crew, Flight

airports = ['Lublin', 'Warszawa', 'Wroclaw', 'Opole', 'Krakow', 'Poznan', 'Szczecin', 'Gdansk', 'Radom', 'Zamosc',
            'Zakopane', 'Bialystok', 'Lodz', 'Targowek', 'Modlin']
first_names = ['Marcin', 'Eliza', 'Anna', 'Malgorzata', 'Ewelina', 'Marek', 'Mateusz', 'Janusz', 'Blazej', 'Genowefa',
              'Bartlomiej', 'Jakub', 'Urszula', 'Waldemar', 'Pawel']
last_names = ['Kartofel', 'Urban', 'Pomidor', 'Katana', 'Pomponik', 'Guzik', 'Rondelek', 'Nicpon', 'Tenteges',
                'Bigos', 'Osiol', 'Marchewka', 'Radiator', 'Klops']

def initData(self):

        # create user
        user = User.objects.create_user(username="user", password="pass")
        user.first_name = first_names[5]
        user.last_name = last_names[3]
        user.save()

        # create two airplanes
        airplane1 = Airplane.objects.create(number=1, capacity=50)
        airplane2 = Airplane.objects.create(number=2, capacity=50)

        # create two crews
        crew1 = Crew.objects.create(captain_first_name=first_names[0], captain_last_name=last_names[0])
        crew2 = Crew.objects.create(captain_first_name=first_names[1], captain_last_name=last_names[1])


        # create two flights
        flight1 = Flight.objects.create(airplane=airplane1, crew=crew1, source="airport1", destination="airport2",
                                        departure_time=self.currentDate, arrival_time=self.currentDate + timedelta(hours=4))

        flight2 = Flight.objects.create(airplane=airplane2, crew=crew2, source="airport1", destination="airport2",
                                        departure_time=self.currentDate, arrival_time=self.currentDate + timedelta(hours=4))

class UnitTest(TestCase):

    def setUp(self):
        self.currentDate = timezone.now()
        super(UnitTest, self).setUp()
        initData(self)


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
        crew3 = Crew.objects.create(captain_first_name=first_names[2], captain_last_name=last_names[2])

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


# PATH=$PATH:/path/to/directory/containing/geckodriver
class SeleniumTest(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.currentDate = timezone.now()
        super(SeleniumTest, self).setUp()
        initData(self)

    def tearDown(self):
        self.selenium.quit()
        super(SeleniumTest, self).tearDown()

    def test_login(self):
        selenium = self.selenium

        # go to main page
        selenium.get("{}/".format(self.live_server_url))

        # sign in
        selenium.find_element_by_id('id_login_button').click()
        selenium.find_element_by_id('username').send_keys("user")
        selenium.find_element_by_id('password').send_keys("pass")
        selenium.find_element_by_id('id_submit_button').click()

        # check the returned result
        assert 'You are logged in' in selenium.page_source

        # go to flight detail page
        selenium.get('{}/airport/flight/1/'.format(self.live_server_url))

        # buy a ticket
        selenium.find_element_by_id('id_buy_ticket_button').click()
        assert 'You bought a ticket for this flight' in selenium.page_source
        user = User.objects.all()[0]
        assert '{} {}'.format(user.first_name, user.last_name) in selenium.page_source

        # selenium.find_element_by_id('id_crew_management_button').click()
        selenium.get('{}/static/airport/crewManagement.html'.format(self.live_server_url))

        # sign in in Crew Management
        selenium.find_element_by_id('id_modal_open_button').click()
        selenium.find_element_by_id('id_login_username').send_keys("user")
        selenium.find_element_by_id('id_login_password').send_keys("pass")
        selenium.find_element_by_id('id_login_button').click()
        assert 'Logged in as' in selenium.page_source

        # try to assign crew1 to flight2 (they are already assigned to flight1 which is in the same time)
        Select(selenium.find_element_by_id('id_flight_select')).select_by_index(1)
        Select(selenium.find_element_by_id('id_crew_select')).select_by_index(0)
        selenium.find_element_by_id('id_assign_button').click()
        # need to wait until page with error message loads
        try:
            WebDriverWait(selenium, 10).until(expected_conditions.presence_of_element_located((By.ID, "id_alert_panel")))
        finally:
            assert 'Could not assign crew to this flight' in selenium.page_source

