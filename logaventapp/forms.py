from django import forms
from django.forms import ModelForm
from logaventapp.models import Event, Example, Logistics, Dudeevent

class CreateEvent (ModelForm):
  class Meta:
    model = Event
    fields = ['title', 'description', 'eventdate', 'eventtime', 'ispublic', 'expectedpplno', 'image', 'budget']

class CreateLogs (ModelForm):
  class Meta:
    model = Logistics
    fields = ['name', 'quantity', 'cost', 'procured']

class CreateDudeevent (ModelForm):
  class Meta:
    model = Dudeevent
    fields = ['name', 'email', 'hpno']