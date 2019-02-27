from django.shortcuts import render
from rest_framework.generics import ListAPIView
from events.models import Event
from .serializers import EventListSerializer

class EventListView(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventListSerializer
