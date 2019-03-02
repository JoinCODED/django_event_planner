from django import forms
from django.contrib.auth.models import User
from .models import Event, Booking, Profile
import datetime
from tempus_dominus.widgets import DateTimePicker


class UserSignup(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ,'password']
        widgets={
        'password': forms.PasswordInput(),
        }


class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['organizer',]
        widgets = {
            'dateandtime':forms.DateTimeInput(attrs={'type':'date'}),
            'time':forms.DateTimeInput(attrs={'type':'time'}),
        }


class BokingForm(forms.ModelForm):
  class Meta:
    model = Booking
    exclude = ['user', 'event']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    exclude = ['user']