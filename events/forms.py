from django import forms
from django.contrib.auth.models import User
from .models import Event, Booking 
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
    # date = forms.DateTimeField(
    #     widget=DateTimePicker(
    #         options={
    #             'minDate': (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),  # Tomorrow
    #             'useCurrent': True,
    #             'collapse': False,
    #         },
    #         attrs={
    #            'append': 'fa fa-calendar',
    #            'input_toggle': False,
    #            'icon_toggle': True,
    #         }
    #     ),
    # )
    class Meta:
        model = Event
        exclude = ['organizer',]

        widgets = {
            'date':forms.DateTimeInput(attrs={'type':'date'}),
        }

    #def clean_date(self):
       # print("HI")
       # date = str(self.cleaned_data['date'])
       # print(date)
       # year = date[:4]
       # print("year", year)
       # month = date[6:8]
       # print("month", month)
       # day = date[3:5]
       # print("day", day)
       # if len(date)==19:
       #     hour = date[11:13]
       #     print("hour", hour)
       #     minutes = date[14:16]
       #     print("minutes", minutes)
       # else:
       #     hour = date[11]
       #     print("hour", hour)
       #     minutes = date[13:15]
       #     print("minutes", minutes)

       # datetime_obj = datetime.datetime(int(year), int(month), int(day), int(hour), int(minutes))
       # print(datetime_obj)
       # return datetime_obj

