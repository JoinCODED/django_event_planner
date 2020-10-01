from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Event(models.Model):
  event_name=models.CharField(max_length=100)
  event_starttime=models.DateTimeField(auto_now_add=True)
  event_endtime=models.DateField(default=now,editable=True)
  def __str__(self):
    return f'{self.event_name}'
    
