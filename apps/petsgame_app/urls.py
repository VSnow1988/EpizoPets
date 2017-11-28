from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
     url(r'^$', views.index),
     url(r'^register', views.register),
     url(r'^login', views.login),
     url(r'^logout', views.logout, name="logout"),
     url(r'^dashboard', views.dashboard, name="dashboard"),
     url(r'^eatconfirm', views.eatconfirm, name="confirmeat"),
     url(r'^eat', views.eat),
     url(r'^newpet', views.newpet, name="newpet"),
     url(r'^addpet', views.addpet, name="addpet"),
	 url(r'^forage', views.forage),
	 url(r'^useitem', views.useitem),
	 url(r'^help', views.help, name="help"),
	 url(r'^hunt', views.hunt, name="hunt"),
	 url(r'^death', views.death, name="death"),
	 url(r'^hunt', views.hunt, name="hunt"),
	 url(r'^huntkeep', views.huntkeep, name="huntkeep"),
	 url(r'^huntkill', views.huntkill, name="huntkill"),
	 url(r'^attack', views.attack, name="attack"),
	 url(r'^catchsecret', views.catchsecret, name="catchsecret")
 ]
