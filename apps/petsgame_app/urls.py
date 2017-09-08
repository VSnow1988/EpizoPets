from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
     url(r'^main', views.index),
     url(r'^register', views.register),
     url(r'^login', views.login),
     url(r'^logout', views.logout, name="logout"),
     url(r'^dashboard', views.dashboard),
     url(r'^eatconfirm', views.eatconfirm, name="confirmeat"),
     url(r'^eat', views.eat),
     url(r'^newpet', views.newpet, name="newpet"),
     url(r'^addpet', views.addpet, name="addpet"),
	 url(r'^forage', views.forage),
	 url(r'^useitem', views.useitem),
 ]
