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
	 )


urlpatterns = [
	path('', home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('event/create/',event_create ,name='create'),
    path('event/list/', event_list ,name='list'),
    path('dashboard/', dashboard ,name='dashboard'),
    path('event/detail/<int:event_id>', event_detail, name='detail'),
    path('event/update/<int:event_id>', event_update, name='update'),
    path('event/delete/<int:event_id>', event_delete, name='delete'),
]