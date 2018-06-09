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


class Crew(models.Model):
    captain_first_name = models.CharField(max_length=20)
    captain_last_name = models.CharField(max_length=20)

    class Meta:
        unique_together = ('captain_first_name', 'captain_last_name')

    def __str__(self):
        return 'Crew of captain %s %s' % (self.captain_first_name, self.captain_last_name)


class Flight(models.Model):
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE, blank=True, null=True, default=None)
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
        if self.departure_time + timedelta(minutes=30) >= self.arrival_time:
            raise ValidationError("Departure time should be at least 30 minutes before arrival time.")

        flights = Flight.objects.exclude(pk=self.pk)
        flights_overlapping = flights.filter(
            Q(departure_time__range=[self.departure_time, self.arrival_time]) |
            Q(arrival_time__range=[self.departure_time, self.arrival_time]))
        if flights_overlapping.filter(airplane=self.airplane).exists():
            raise ValidationError("The airplane has already planned flight in this time.")

        # check if this airplane won't have more than 4 flights in this day after adding this flight:
        if self.departure_time.day == self.arrival_time.day:
            # Option 1: This flight is all in one day

            # get all flights of this plane in this day
            flights_this_day = Flight.objects.filter(airplane=self.airplane).filter(
                Q(departure_time__day=self.departure_time.day) | Q(departure_time__day=self.arrival_time.day))
            if len(flights_this_day) > 4:
                raise ValidationError("This airplane has already 4 flights planned for this day.")
        else:
            # Option 2: This flight starts in one day and ends in next day

            flights_starting_this_day = Flight.objects.filter(airplane=self.airplane).filter(
                Q(departure_time__day=self.departure_time.day) | Q(departure_time__day=self.arrival_time.day))
            flights_ending_this_day = Flight.objects.filter(airplane=self.airplane).filter(
                Q(arrival_time__day=self.departure_time.day) | Q(arrival_time__day=self.arrival_time.day))

            if len(flights_starting_this_day) > 4:
                raise ValidationError("This airplane has already 4 flights planned for this day.")

            if len(flights_ending_this_day) > 4:
                raise ValidationError("This airplane has already 4 flights planned for this day.")


        if flights.exclude(pk=self.pk) \
                .filter(Q(departure_time__range=[self.departure_time, self.arrival_time])
                        | Q(arrival_time__range=[self.departure_time, self.arrival_time])) \
                .filter(crew=self.crew).exists():
            raise ValidationError("This crew has another flight in this time.")

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
