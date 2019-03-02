from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import (
UserSignup,
UserLogin,
EventForm,
BokingForm,
UserForm,
ProfileForm,
)
from .models import Event, Booking, Profile
import datetime
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.models import User


def home(request):
    events = Event.objects.all().filter(dateandtime__gte = datetime.datetime.today()).order_by('dateandtime')[:3]

    context = {
    'events': events,
    }
    return render(request, 'home.html', context)

class Signup(View):
    form_class = UserSignup 
    profile_form_class = ProfileForm
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        form2 = self.profile_form_class()
        return render(request, self.template_name, {'form': form , 'form2': form2})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form2 = self.profile_form_class(request.POST, request.FILES)
        if form.is_valid() and form2.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            prot = form2.save(commit=False)
            prot.user = user
            prot.save()
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

def event_create(request):
    form = EventForm(request.POST, request.FILES)
    if form.is_valid():
        event = form.save(commit=False)
        event.organizer = request.user
        event.save()
        return redirect('list')
    print(form.errors)
    


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
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('list')
        print(form.errors)
    events = Event.objects.filter(organizer= request.user)
    # events = request.user.organized.all()


    context = {
    "events": events,
    "form":form,
    
    }
    return render(request, 'dashboard.html', context)

def chart_data(request):
    lables = [['Task', 'Hours per Day'],]
    for event in request.user.organized.all():
        print('--'*30)
        print([event.name, event.bookings.count()])
        lables.append([event.name, event.bookings.count()])
    print(lables)
    response = {
        "event" : lables,
    }
    return JsonResponse(response, safe=False)


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
    tagc = "alert alert-danger alert-dismissible fade show"
    if number_of_tickets_b <= rem_number_of_tickets:
        booking = Booking(user=request.user, event=event_obj, number_of_booking=num_b)
        booking.save()
        rem_number_of_tickets -= num_b
        mass = "You have booked successfully."
        tagc = "alert alert-success alert-dismissible fade show"
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

# remove and taje away URLS
def update_profile(request):
    user_form = UserForm(request.POST, instance=request.user)
    if user_form.is_valid():
        user_form.save()
        messages.success(request, ('Your profile was successfully updated!'))
        return redirect('profile')
    return redirect('profile')

#remove 
def create_profile(request):
    if request.user.is_anonymous:
        return redirect('login')
    form = ProfileForm()
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('home')
    context = {
        "form":form,
    }
    return render(request, 'create-profile.html', context)
    

def profile(request, user_id):
    if request.user.is_anonymous:
        return redirect('login')
    user_obj = User.objects.get(id=user_id)
    user_form = UserForm(instance=user_obj)
    profile_obj = Profile.objects.get(user=user_obj)
    profile_update_form = ProfileForm(instance=profile_obj)
    events = Event.objects.filter(organizer= user_obj)
    if request.method == "POST": 
        user_form = UserForm(request.POST, instance=user_obj)
        profile_update_form = ProfileForm(request.POST, request.FILES, instance=profile_obj)
        if user_form.is_valid() and profile_update_form.is_valid():
            user_form.save()
            profile_update_form.save()
            return redirect('profile', user_id)
    context = {
        "user": user_obj,
        "user_form": user_form,
        "events": events,
        "Profile": profile_obj,
        "profile_update_form": profile_update_form,
    }
    return render(request, 'profile.html', context)



def booking_delete(request, event_id):
    if request.user.is_anonymous:
        return redirect('login')
    now = datetime.datetime.now()
    event_obj = Event.objects.get(id=event_id)
    my_booking = Booking.objects.filter(event=event_obj).filter(user=request.user)
    event_time_hour = event_obj.time.hour
    today = event_obj.dateandtime.day
    month = event_obj.dateandtime.month
    year = event_obj.dateandtime.year
    # print(today)
    # print(month)
    # print(year)
    print(event_obj.time.hour - now.hour)
    #if  (now.hour+3) > event_time_hour: 
        #my_booking.delete()
    
        
    return redirect('my_booking')


