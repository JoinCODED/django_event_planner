from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



class Event(models.Model):
    name = models.CharField(max_length = 120)

    description = models.TextField()
    number_of_tickets = models.IntegerField()
    cho_state = (

            ('SOON' , 'SOON'),
            ('OPEN' , 'OPEN'),
            ('CLOSE' , 'CLOSE'),
        )

    
    state = models.CharField(
            max_length = 5,
            choices = cho_state,
            default =  'SOON',
        )
    organizer = models.ForeignKey(User,  on_delete=models.CASCADE, related_name= 'organized')

    poster = models.ImageField(upload_to='event_logos', null=False, blank=False)


    def __str__ (self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'event_id': self.id})


class Booking(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE, related_name= 'subscriber')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
