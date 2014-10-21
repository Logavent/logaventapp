from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotModified
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from datetime import datetime
# Import models
from logaventapp.models import Event, Example, Logistics, Dudeevent
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import CreateEvent, CreateLogs, CreateDudeevent
from django.core.mail import send_mail
from logavent import settings

#######################################################################
################################ INDEX ################################
#######################################################################
def index(request):
  #Obtain the context from the HTTP request, whatever that means
  c = RequestContext(request)  
  #dictionary for infomrmation
  popular_events = Event.objects.filter(ispublic=True).order_by('-pplno')[:6]
  latest_events = Event.objects.filter(ispublic=True).order_by('-datetimecreated')[:2]                                              
  d = {'popular_events': popular_events, 'latest_events': latest_events}
  for event in popular_events:
        event.url = "event/" + event.title.replace(' ', '_')
  for event in latest_events:
        event.url = "event/" + event.title.replace(' ', '_')
  return render_to_response('index.html', d, c)

#def search(request):
  #c = RequestContext(request)
  #if request.method != 'POST':
  #  return HttpResponseRedirect('http://logavent-cep-33-142474.apse1.nitrousbox.com/')
  #else:
  #  stext = request.POST['search_text']
  #  try:
  #    event = Event.objects.filter(title=stext)
  #    d = {'event':event}
  #  except Event.DoesNotExist:
  #    d = {'event':None, 'stext':stext}
  #return render_to_response('search.html', d, c)

#######################################################################
######################## DISPLAY ALL EVENTS ###########################
#######################################################################
def all_events(request):
  #Obtain the context from the HTTP request, whatever that means
  c = RequestContext(request)  
  #dictionary for infomrmation
  all_events = Event.objects.filter(ispublic=True).order_by('-pplno')
  d = {'all_events': all_events}
  for event in all_events:
        event.url = "event/" + str(event.pk)
  return render_to_response('all_events.html', d, c)

#def handle_uploaded_file(f):
#    with open('media/', 'wb+') as destination:
#        for chunk in f.chunks():
#            destination.write(chunk)
            
#def uploadImage (request):
#  if request.method == 'POST':
#        form = CreateEvent(request.POST, request.FILES)
#        if form.is_valid():
#            handle_uploaded_file(request.FILES['file'])
#            return HttpResponseRedirect('dashboard/')
#  else:
#    form = UploadFileForm()
#  return render_to_response('event.html', {'form': form})
#######################################################################
########################### DISPLAY EVENT #############################
#######################################################################
def event(request, event_url):
  c = RequestContext(request)
  d = {}
  event = get_object_or_404(Event, pk=event_url)
  register_url = "http://logavent-cep-33-142474.apse1.nitrousbox.com/event/" + str(event.pk) + "/register/"
  event.manage_url = "http://logavent-cep-33-142474.apse1.nitrousbox.com/manage_event/" + str(event.pk) + "/"
  event.pplno = len(Dudeevent.objects.filter(event=event, isauth=True))
  event.save()
  if event.pplno == 1:
    isone = True
  else:
    isone = False
  d = {'event':event, 'register_url':register_url, 'isone':isone}
  return render_to_response('event.html', d, c)

def register_for_event(request, event_url):
  c = RequestContext(request)
  event = get_object_or_404(Event, pk=event_url)
  register_url = "http://logavent-cep-33-142474.apse1.nitrousbox.com/event/" + str(event.pk) + "/register/"
  if request.method=='POST':
    newdude = Dudeevent()
    newdude.event = event
    newdude.name = request.POST['name']
    newdude.email = request.POST['email']
    if request.POST['hpno'] != "":
      newdude.hpno = request.POST['hpno']
    newdude.save()
    send_mail('Authentication for joining event', 'Hi '+newdude.name+',\n\nYou have signed up for "'+event.title+'". Please click on this link to confirm your participation: \n\nhttp://logavent-cep-33-142474.apse1.nitrousbox.com/event/'+ str(event.pk) + '/'+str(newdude.pk)+'/'+'auth\n\nThank you\nThe Logavent Team', settings.EMAIL_HOST_USER, [newdude.email], fail_silently=False)
  event.pplno = len(Dudeevent.objects.filter(event=event, isauth=True))
  event.save()
  if event.pplno == 1:
    isone = True
  else:
    isone = False
  d = {'event':event, 'register_url':register_url, 'isone':isone}
  return render_to_response('event.html', d, c)

def auth_dude(request, event_url, dude_url):
  c = RequestContext(request)
  event = get_object_or_404(Event, pk=event_url)
  event.pplno = len(Dudeevent.objects.filter(event=event, isauth=True))
  event.save()
  if event.pplno == 1:
    isone = True
  else:
    isone = False
  register_url = "http://logavent-cep-33-142474.apse1.nitrousbox.com/event/" + str(event.pk) + "/register/"
  d = {'event':event, 'register_url':register_url, 'isone':isone}
  dude = get_object_or_404(Dudeevent, pk=dude_url)
  dude.isauth = True
  dude.save()
  return render_to_response('event.html', d, c)

@login_required
def remove_dude(request,event_url,dude_url):
  event = get_object_or_404(Event, pk=event_url)
  dude = get_object_or_404(Dudeevent, pk=dude_url, event=event)
  dude.delete()
  return HttpResponseRedirect('http://logavent-cep-33-142474.apse1.nitrousbox.com/manage_event/' + str(event.pk))
#######################################################################
############################## DASHBOARD ##############################
#######################################################################
def dashboard(request):
  #Obtain the context from the HTTP request, whatever that means
  c = RequestContext(request)
  eventlist = []
  eventcount = 0
  pplcount = 0
  for i in Event.objects.all():
    if i.organiser == request.user:
      eventlist += [i]
      eventcount += 1
      i.pplno = len(Dudeevent.objects.filter(event=i, isauth=True))
      i.save()
      pplcount += i.pplno
  if eventcount == 1:
    eisone = True
  else:
    eisone = False
  if pplcount == 1:
    pisone = True
  else:
    pisone = False
  #dictionary for infomrmation
  d = {'eventlist':eventlist, 'eventcount':eventcount, 'pplcount':pplcount, 'eisone':eisone, 'pisone':pisone}
  for event in eventlist:
        event.manage_url = "manage_event/" + str(event.pk)
  return render_to_response('dashboard.html', d, c)

#######################################################################
############################ MANAGE EVENTS ############################
#######################################################################
@login_required
def manage_event(request, event_url):
  c = RequestContext(request)
  spent = 0
  event = get_object_or_404(Event, pk=event_url)
  loglist = Logistics.objects.filter(event=event)
  log_create_url = "http://logavent-cep-33-142474.apse1.nitrousbox.com/create_logs/" + str(event.pk) + "/"
  for i in loglist:
    spent += i.totalcost
    i.edit_url = "http://logavent-cep-33-142474.apse1.nitrousbox.com/edit_logs/" + str(event.pk) + "/" + str(i.pk) + "/"
    i.del_url = "http://logavent-cep-33-142474.apse1.nitrousbox.com/delete_logs/" + str(event.pk) + "/" + str(i.pk) + "/"
  registereddudes = Dudeevent.objects.filter(event=event, isauth=True)
  for j in registereddudes:
    j.del_url = "http://logavent-cep-33-142474.apse1.nitrousbox.com/event/" + str(event.pk) + "/" + str(j.pk) + "/remove/"
  event.edit_url = "http://logavent-cep-33-142474.apse1.nitrousbox.com/edit_event/" + str(event.pk) + "/"
  event.public_url = "http://logavent-cep-33-142474.apse1.nitrousbox.com/event/" + str(event.pk) + "/"
  extra = event.budget-spent
  d = {'daevent':event, 'loglist':loglist, 'log_create_url':log_create_url, 'registereddudes':registereddudes, 'spent':spent, 'extra':extra}
  return render_to_response('manage_event.html', d, c)

@login_required
def edit_event(request, event_url):
  c = RequestContext(request)
  daevent = get_object_or_404(Event, pk=event_url)  
  # A HTTP POST?
  if request.method == 'POST':
    form = CreateEvent(request.POST, request.FILES, instance=daevent)
    # Have we been provided with a valid form?
    if form.is_valid():
      # make a newevent and input form data into newevent; since commit=False. If commit=true it directly saves the form as an event
      form.save()
      daevent.datetimecreated = datetime.now()
      # Save the new category to the database.
      daevent.save()
      # Now call the dashboard() view.
      # The user will be shown the dashboard.
      return HttpResponseRedirect('http://logavent-cep-33-142474.apse1.nitrousbox.com/manage_event/'+str(daevent.pk)+'/')
    else:
      # The supplied form contained errors - just print them to the terminal.
      d = {'errors':form.errors, 'daevent':daevent}
  else:
    form = CreateEvent(instance=daevent)
    #dictionary for information
    d = {'errors':None, 'daevent':daevent}
  return render_to_response('edit_event.html', d, c)

@login_required
def create_event(request):
  #Obtain the context from the HTTP request, whatever that means
  c = RequestContext(request)
  # A HTTP POST?
  if request.method == 'POST':
      form = CreateEvent(request.POST, request.FILES)
      # Have we been provided with a valid form?
      if form.is_valid():
        # make a newevent and input form data into newevent; since commit=False. If commit=true it directly saves the form as an event
        newevent = form.save(commit=False)
        newevent.organiser = request.user
        newevent.datetimecreated = datetime.now()
        # Save the new category to the database.
        newevent.save()
        # Now call the dashboard() view.
        # The user will be shown the dashboard.
        return HttpResponseRedirect('http://logavent-cep-33-142474.apse1.nitrousbox.com/manage_event/'+str(newevent.pk)+'/')
      else:
          # The supplied form contained errors - just print them to the terminal.
          d = {'errors':form.errors}
  else:
    #form = CreateEvent()
    #dictionary for information
    d = {'errors':None}
  return render_to_response('create_event.html', d, c)

@login_required
def delete_event(request,event_url):
  daevent = get_object_or_404(Event, pk=event_url)
  if request.user == daevent.organiser:
    #delete ppl who have registered for this event
    Dudeevent.objects.filter(event=daevent).delete()
    #delete logs of this event
    Logistics.objects.filter(event=daevent).delete()
    #delete the event itself. Sayonara!
    daevent.delete()
  return HttpResponseRedirect('http://logavent-cep-33-142474.apse1.nitrousbox.com/dashboard')
#######################################################################
############################# MANAGE LOGS #############################
#######################################################################
@login_required
def edit_logs(request,event_url,log_url):
  c = RequestContext(request)
  daevent = get_object_or_404(Event, pk=event_url)
  log = get_object_or_404(Logistics, pk=log_url, event=daevent)
  if request.method=='POST':
    logname = request.POST['name'].lower()
    log.name = logname
    logquantity = request.POST['quantity']
    log.quantity = logquantity
    log.event = daevent
    if request.POST.get('procured')!= None:
      log.procured = True
    else:
      log.procured = False
    logcost = request.POST['cost']
    log.cost = logcost
    log.totalcost = float(logcost)*int(logquantity)
    log.save()
    return HttpResponseRedirect("http://logavent-cep-33-142474.apse1.nitrousbox.com/manage_event/" + str(daevent.pk) + "/")
  else:
    edit_url = "http://logavent-cep-33-142474.apse1.nitrousbox.com/edit_logs/" + str(daevent.pk) + "/" + log_url + "/"
    d = {'daevent':daevent, 'log':log, 'edit_url':edit_url}
  return render_to_response('edit_logs.html', d, c) 

@login_required
def create_logs(request,event_url):
  c = RequestContext(request)
  daevent = get_object_or_404(Event, pk=event_url)
  create_url = "http://logavent-cep-33-142474.apse1.nitrousbox.com/create_logs/" + event_url + "/"
  d = {'create_url':create_url, 'daevent':daevent}
  
  if request.method=='POST':
    newlog = Logistics()
    newlog.name = request.POST['name'].lower()
    newquantity = request.POST['quantity']
    newlog.quantity = newquantity
    newlog.event = daevent
    if request.POST.get('procured')!= None:
      newlog.procured = True
    else:
      newlog.procured = False
    newcost = request.POST['cost']
    newlog.cost = newcost
    newlog.totalcost = float(newcost)*int(newquantity)
    newlog.save()
    return HttpResponseRedirect("http://logavent-cep-33-142474.apse1.nitrousbox.com/manage_event/" + str(daevent.pk) + "/") 
  else:
    return render_to_response('create_logs.html', d, c)   

@login_required
def delete_logs(request,event_url,log_url):
  daevent = get_object_or_404(Event, pk=event_url)
  log = get_object_or_404(Logistics, pk=log_url, event=daevent)
  log.delete()
  return HttpResponseRedirect('http://logavent-cep-33-142474.apse1.nitrousbox.com/manage_event/' + str(daevent.pk))
#######################################################################
############################## USER AUTH ##############################
#######################################################################
def log_in(request):
  c = RequestContext(request)
  username = request.POST['username']
  password = request.POST['password']
  user = authenticate(username=username, password=password)
  if user is not None:
      if user.is_active:
          login(request, user)
          return HttpResponseRedirect('/dashboard')
          # Redirect to a success page.
      else:
          return HttpResponse("Invalid login details supplied.")
  else:
    # Return an 'invalid login' error message.
    print "Invalid login details: {0}, {1}".format(username, password)
    return HttpResponse("Invalid login details supplied.")

def log_out(request):
  # Since we know the user is logged in, we can now just log them out.
  logout(request)
  return HttpResponseRedirect('/')  
  
def sign_up(request):
  c = RequestContext(request)
  if request.method=='POST':
    haveerrors = False
    errorlist = []
    username = request.POST['susername']
    email = request.POST['semail']
    password = request.POST['spassword']
    passwordcheck = request.POST['spasswordcheck']
    userlist = []
    for i in User.objects.all():
      userlist += [i.username]
    if username in userlist:
      useralrtaken = "The username " +username+" has already been taken."
      errorlist += [useralrtaken]
      haveerrors = True
    if password != passwordcheck:
      pwcheck = "Your passwords didn't match"
      errorlist += [pwcheck]
      haveerrors = True
    if haveerrors==False:
      User.objects.create_user(username, email, password)
      user = authenticate(username=username, password=password)
      login(request, user)
      return HttpResponseRedirect('/dashboard')
    else:
      d = {'errors':errorlist}
  else: 
    d = {'errors':None}
  return render_to_response('sign-up.html', d, c) 