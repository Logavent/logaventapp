from django.contrib import admin
#importing UserProfile
from logaventapp.models import Event, Example, Logistics, Dudeevent

# Register your models here.
admin.site.register(Event)
admin.site.register(Example)
admin.site.register(Logistics)
admin.site.register(Dudeevent)