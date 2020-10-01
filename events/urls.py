from django.urls import path
from .views import Login, Logout, Signup, home, event

urlpatterns = [
	path('', home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
	path('event/' event, name='event),
]
