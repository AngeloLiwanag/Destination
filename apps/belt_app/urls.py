from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^dashboard$', views.success),
    url(r'^login$', views.login),
    url(r'^trips/new$', views.create), #create page
    url(r'^make$', views.make),
    url(r'^destroy/(?P<one_trip_id>\d+)$', views.delete), #delete
    url(r'^trips/edit/(?P<one_trip_id>\d+)$', views.edit), 
    url(r'^update/(?P<trip_id>\d+)$', views.update),
    url(r'^trips/(?P<one_trip_id>\d+)$', views.read),
]