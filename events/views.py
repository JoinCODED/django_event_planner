from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin, EventForm
from .models import Event
import datetime
from django.contrib import messages


def home(request):

    
    return render(request, 'home.html')

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

    events = Event.objects.all().filter(dateandtime__gte = datetime.datetime.today() )
    
    context = {
    'events': events
    }

    return render(request, 'list.html', context)


def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    context = {
        "event": event,
    }
    return render(request, 'detail.html', context)


def dashboard(request):
    events = Event.objects.all().filter(organizer= request.user)

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