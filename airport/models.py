from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import timedelta

class Airplane(models.Model):
    # number = models.CharField(max_length=10, unique=True)
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField()

    def __str__(self):
        return 'Airplane no %s' % self.number

    def clean(self):
        if (self.capacity < 20):
            raise ValidationError('Airplane must have at least 20 places')

class Flight(models.Model):
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    #TODO maybe I should create airport model instead of just naming airports
    source = models.CharField(max_length=20)
    destination = models.CharField(max_length=20)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        # TODO complete return string
        return 'Flight from %s to %s' % (self.source, self.destination)

    def clean(self):
        #TODO check all requirements
        pass

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    #TODO check unique name of passenger or add an unique id

    def __str__(self):
        return 'Passenger %s %s' % (self.first_name, self.last_name)

class Ticket(models.Model):
    passenger = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)

    def clean(self):
        #TODO check if there are still free places in flight before creating the ticket
        pass


