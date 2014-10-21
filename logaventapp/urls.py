from django.conf.urls import patterns, url
from logaventapp import views

urlpatterns = patterns('',
        #index
        url(r'^$', views.index, name='index'),
        #display events
        url(r'^events', views.all_events, name='events'),
        #url(r'^events/search', views.search, name='search'),
        url(r'^event/(?P<event_url>\d+)/$', views.event, name='event'),
        url(r'^event/(?P<event_url>\d+)/register/$', views.register_for_event, name='register_for_event'),
        url(r'^event/(?P<event_url>\d+)/(?P<dude_url>\d+)/auth', views.auth_dude, name='auth_dude'),
        url(r'^event/(?P<event_url>\d+)/(?P<dude_url>\d+)/remove', views.remove_dude, name='remove_dude'),
        #dashboard 
        url(r'^dashboard', views.dashboard, name='dashboard'),
        #manage events
        url(r'^create_event', views.create_event, name='create_event'),
        url(r'^edit_event/(?P<event_url>\d+)/$', views.edit_event, name='edit_event'),
        url(r'^manage_event/(?P<event_url>\d+)/$', views.manage_event, name='manage_event'),
        url(r'^delete_event/(?P<event_url>\d+)/$', views.delete_event, name='delete_event'),
        #manage logs 
        url(r'^edit_logs/(?P<event_url>\d+)/(?P<log_url>\d+)/$', views.edit_logs, name='edit_logs'),
        url(r'^delete_logs/(?P<event_url>\d+)/(?P<log_url>\d+)/$', views.delete_logs, name='delete_logs'),
        url(r'^create_logs/(?P<event_url>\d+)/$', views.create_logs, name='create_logs'),
        #user autH
        url(r'^log_out',views.log_out, name='log_out'),
        url(r'^log_in',views.log_in, name='log_in'),
        url(r'^sign_up', views.sign_up, name='sign_up'),
)