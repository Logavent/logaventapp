from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
  title = models.CharField(max_length=35)
  organiser = models.ForeignKey(User)
  description = models.CharField(max_length=7000)
  eventdate = models.DateField(default=None)
  eventtime = models.TimeField(default=None)
  datetimecreated = models.DateTimeField(default=None)
  ispublic = models.BooleanField(default=False)
  pplno = models.IntegerField(default=0)
  expectedpplno = models.IntegerField(default=1)
  image = models.ImageField(upload_to='event_images/', blank=True)
  budget = models.DecimalField(max_digits=99999999, decimal_places=2, default=None)
  
# suggested categories; friend requests...?; notifications...?;
  def __unicode__(self):
      return self.title

class Dudeevent(models.Model):
  event = models.ForeignKey('Event')
  name = models.CharField(max_length=35)
  email = models.EmailField()
  hpno = models.CharField(max_length=8, blank=True)
  isauth = models.BooleanField(default=False)
  
  def __unicode__(self):
    return self.name+" has registered for "+self.event.title
  
class Example(models.Model):
  title = models.CharField(max_length=1)
  def __unicode__(self):
      return self.title
    
class Logistics(models.Model):
  name = models.CharField(max_length=100)
  quantity = models.DecimalField(max_digits=99999999, decimal_places=0)
  event = models.ForeignKey('Event')
  procured = models.BooleanField(default=False)
  cost = models.DecimalField(max_digits=99999999, decimal_places=2)
  totalcost = models.DecimalField(max_digits=99999999, decimal_places=2)
  def __unicode__(self):
      return self.name
  