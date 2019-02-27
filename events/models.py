from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver



class Event(models.Model):
    name = models.CharField(max_length = 120)
    dateandtime = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    number_of_tickets = models.IntegerField()
    cho_place = (
            ('Choose City' , 'Choose City'),
            ('Riyadh' , 'Riyadh'),
            ('Jeddah' , 'Jeddah'),
            ('Dammam' , 'Dammam'),
            ('Makkah' , 'Makkah'),

        )
    place = models.CharField(
            max_length = 12,
            choices = cho_place,
            default =  'Choose City',
        )
    organizer = models.ForeignKey(User,  on_delete=models.CASCADE, related_name= 'organized')
    poster = models.ImageField(upload_to='event_logos', null=False, blank=False)

    def __str__ (self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'event_id': self.id})

    def seats_left(self):
        return self.number_of_tickets - sum(self.bookings.all().values_list('number_of_booking', flat=True))


class Booking(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='bookings')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    number_of_booking = models.IntegerField()

    def __str__ (self):
        return ("%s booking for %s" %(self.user.username , self.event.name))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='user_logos')
    description = models.TextField()

    def __str__(self):
        return self.user.first_name




