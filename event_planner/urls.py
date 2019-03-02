"""event_planner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api.views import (
EventListView,
UserCreateView,
EventUpdateView,
EventCreateView,
EventDetailView,
OrganizerEventsView,
)
from rest_framework_jwt.views import obtain_jwt_token



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
    path('api/list/', EventListView.as_view(), name='api-list'),
    path('api/organizer/', EventListView.as_view(), name='api-organizer'),
    path('api/signup/', UserCreateView.as_view(), name='api-signup'),
    path('api/signin/', obtain_jwt_token, name='api-signin'),
    path('api/create/', EventCreateView.as_view(), name='api-create'),
    path('api/update/<int:event_id>/', EventUpdateView.as_view(), name='api-update'),
    path('api/detail/<int:event_id>/', EventDetailView.as_view(), name='api-detail'),
    path('api/organizer/events/', OrganizerEventsView.as_view(), name='organizer-events')
]


if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)