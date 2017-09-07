# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=100)
    birthdate = models.DateField()
    class Meta:
        app_label = "petsgame_app"

class Pet(models.Model):
	id = models.IntegerField(primary_key=True)
	owner = models.ForeignKey(User, null=False)
	name = models.CharField(max_length=100)
	type = models.CharField(max_length=25)
	maxhp = models.IntegerField()
	currenthp = models.IntegerField()
	birthdate = models.DateField(auto_now_add=True)
	class Meta:
		app_label = "petsgame_app"
