import os

def populate():
    python_cat = add_cat('Python')

    add_event(
      title="Official Python Convention",
      nu = "ADadTan",
      d = "Come one come all!",
      ed = "12/12/12",
      et = "12:00 PM",
      dtc = "11/12/12 3:00PM"
      pplno = "12",
      epm = "120",
      bud = "$2000")

    # Print out what we have added to the user.
    for e in Event.objects.all():
            print "- "+str(e)

def add_event(title, nu, d, ed, et, dtc, pplno, epn, bud):
    e = Event.objects.get_or_create(title=title, name_url=nu, description=d, eventdate=ed, eventtime=et, datetimecreated = dtc, pplno = pplno, expectedpplno = epn, budget = bud)[0]
#   eventdate = models.DateField(default=None)
#   eventtime = models.TimeField(default=None)
#   datetimecreated = models.DateTimeField(default=None)
#   pplno = models.IntegerField(default=0)
#   expectedpplno = models.IntegerField(default=1)
#   #image = models.ImageField(upload_to='img/', blank=True)
#   budget = models.DecimalField(max_digits=99999999, decimal_places=2, default=None)
    return e

# Start execution here!
if __name__ == '__main__':
    print "Populating the table with bogus, erm, I mean awesome events..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logavent.settings')
    from logaventapp.models import Events, Logistics
    populate()