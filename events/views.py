from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import (
UserSignup,
UserLogin,
EventForm,
BokingForm,
UserForm,
)
from .models import Event, Booking
import datetime
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q




def home(request):
    events = Event.objects.all().filter(dateandtime__gte = datetime.datetime.today()).order_by('dateandtime')[:3]

    context = {
    'events': events,
    }
    return render(request, 'home.html', context)

class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("home")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                return redirect('dashboard')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")


# def clean_date(date):
#         # print(date)
#         year = date[6:10]
#         # print("year", year)
#         month = date[:2]
#         # print("month", month)
#         day = date[3:5]
#         # print("day", day)
#         if len(date)==19:
#             hour = date[11:13]
#             # print("hour", hour)
#             minutes = date[14:16]
#             # print("minutes", minutes)
#         else:
#             hour = date[11]
#             # print("hour", hour)
#             minutes = date[13:15]
#             # print("minutes", minutes)

#         datetime_obj = datetime.datetime(int(year), int(month), int(day), int(hour), int(minutes))
#         # print(datetime_obj)
#         return datetime_obj


def event_create(request):
    if request.user.is_anonymous:
        return redirect('signin')
    form = EventForm()
    if request.method == "POST":
        # print(request.POST)
        # my_date = clean_date(request.POST['date'])
        # my_dict = {
        #     'name': request.POST['name'],
        #     'description': request.POST['description'],
        #     'date': my_date,
        #     'number_of_tickets': request.POST['number_of_tickets'],
        #     'state': request.POST['state'],
        #     'poster': request.FILES['poster'],
        # }
        # my_dict['date'] = my_date
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('home')
        print(form.errors)
    context = {
        "form":form,
    }
    return render(request, 'create.html', context)


def event_list(request):
    formboking = BokingForm()

    events = Event.objects.all().filter(dateandtime__gte = datetime.datetime.today())   
    query = request.GET.get('q')
    if query:
        events = events.filter(
            Q(name__icontains=query)|
            Q(description__icontains=query)|
            Q(organizer__username__icontains=query)
        ).distinct()
    context = {
    'events': events,
    'formboking': formboking,
    }
    return render(request, 'list.html', context)


def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    booked_tickets = Booking.objects.filter(event= event)
    context = {
        "event": event,
        "booked_tickets": booked_tickets,
    }
    return render(request, 'detail.html', context)


def dashboard(request):
    if request.user.is_anonymous:
        return redirect('login')
    events = Event.objects.filter(organizer= request.user)
    # events = request.user.organized.all()

    context = {
    'events': events
    }
    return render(request, 'dashboard.html', context)


def event_update(request, event_id):
    event = Event.objects.get(id=event_id)
    if not (request.user == event.organizer):
        return redirect('login')
    form = EventForm(instance=event)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('list')
    context = {
        "event": event,
        "form":form,
    }
    return render(request, 'update.html', context)

def event_delete(request, event_id):
    event_obj = Event.objects.get(id=event_id)
    if not (request.user == event_obj.organizer):
        return redirect('list')
    event_obj.delete()
    return redirect('list')

def event_booking(request, event_id, num_b):
    if request.user.is_anonymous:
        return redirect('login')

    event_obj = Event.objects.get(id=event_id)
    number_of_tickets_b = num_b
    rem_number_of_tickets = event_obj.seats_left()
    mass = "Your booking more than number of tickets"
    tagc = "alert alert-danger"
    if number_of_tickets_b <= rem_number_of_tickets:
        booking = Booking(user=request.user, event=event_obj, number_of_booking=num_b)
        booking.save()
        rem_number_of_tickets -= num_b
        mass = "You have booked successfully."
        tagc = "alert alert-success"
    elif rem_number_of_tickets == 0 :
        mass = "The Event is full"
        

            
    response = {
        "rem_number_of_tickets": rem_number_of_tickets,
        "mass": mass,
        "tagc": tagc,

    }
    return JsonResponse(response, safe=False)




def previous_event(request):
    bookings = request.user.bookings.filter(event__dateandtime__lte = datetime.datetime.today())
    context = {
    'bookings':bookings
    }
    return render(request, 'previous_event.html', context)


def my_booking(request):
    bookings = request.user.bookings.filter(event__dateandtime__gte = datetime.datetime.today())
    context = {
    'bookings':bookings
    }

    return render(request, 'my_booking.html', context)






def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('profile')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
    context = {
        'user_form': user_form,
    }
    return render(request, 'profile.html', context)



