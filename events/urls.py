from django.urls import path
from .views import (
	 Login,
	 Logout,
	 Signup,
	 home,
	 event_create,
	 event_list,
	 event_detail,
	 dashboard,
	 event_delete,
	 event_update,
	 event_booking,
	 previous_event,
	 my_booking,
	 update_profile,
	 )


urlpatterns = [
	path('', home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('event/create/',event_create ,name='create'),
    path('event/list/', event_list ,name='list'),
    path('profile/', update_profile ,name='profile'),
    path('previous/event/', previous_event ,name='previous_event'),
    path('upcoming/event/', my_booking ,name='my_booking'),
    path('dashboard/', dashboard ,name='dashboard'),
    path('event/detail/<int:event_id>', event_detail, name='detail'),
    path('event/update/<int:event_id>', event_update, name='update'),
    path('event/delete/<int:event_id>', event_delete, name='delete'),
    path('event/booking/<int:event_id>/<int:num_b>/', event_booking, name='booking')
]