from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class Airplane(models.Model):
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField()

    def __str__(self):
        return 'Airplane no %s' % self.number

    def clean(self):
        if (self.capacity < 20):
            raise ValidationError('Airplane must have at least 20 places')


class Flight(models.Model):
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    source = models.CharField(max_length=20)
    destination = models.CharField(max_length=20)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return 'Flight %d from %s (%s) to %s (%s)' % (
            self.pk, self.source, self.departure_time.strftime("%Y-%m-%d %H:%M"), self.destination,
            self.arrival_time.strftime("%Y-%m-%d %H:%M"))

    def clean(self):
        # check if departure time is at least 30 minutes before arrival time
        if self.departure_time + timedelta(minutes=30) <= self.arrival_time:
            raise ValidationError("Departure time should be at least 30 minutes before arrival time.")

        # for all flights of this airplane, check if they don't overlap with new one
        flights = Flight.objects.filter(airplane=self.airplane)
        for flight in flights:
            if not (
                    flight.arrival_time < self.arrival_time and self.arrival_time < flight.departure_time
                    and flight.arrival_time < self.departure_time and self.departure_time < flight.arrival_time):
                raise ValidationError("The airplane has already planned flight in this time.")

        # check if this airplane won't have more than 4 flights in this day after adding this flight:
        if self.departure_time.day == self.arrival_time.day:
            # Option 1: This flight is all in one day

            # get all flights of this plane in this day
            flights_this_day = Flight.objects.filter(airplane=self.airplane).filter(Q(departure_time__day=self.departure_time.day) |  Q(departure_time__day=self.arrival_time))
            if len(flights_this_day) > 4:
                raise ValidationError("This airplane has already 4 flights planned for this day.")
        else:
            # Option 2: This flight starts in one day and ends in next day

            flights_starting_this_day = Flight.objects.filter(airplane=self.airplane).filter(Q(departure_time__day=self.departure_time.day) |  Q(departure_time__day=self.arrival_time))
            flights_ending_this_day = Flight.objects.filter(airplane=self.airplane).filter(Q(arrival_time__day=self.departure_time.day) |  Q(arrival_time__day=self.arrival_time))

            if len(flights_starting_this_day) > 4:
                raise ValidationError("This airplane has already 4 flights planned for this day.")

            if len(flights_ending_this_day) > 4:
                raise ValidationError("This airplane has already 4 flights planned for this day.")


class User(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Ticket(models.Model):
    passenger = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)

    def clean(self):
        # if number of passengers for this flight equals the capacity of the airplane, new ticket cannot be created
        capacity = self.flight.airplane.capacity
        number_of_passengers = len(Ticket.objects.filter(flight=self.flight))
        if capacity <= number_of_passengers:
            raise ValidationError("All places in this airplane are booked up.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Ticket, self).save(*args, **kwargs)
