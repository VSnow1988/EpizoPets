# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
import datetime
import re, random
from models import User, Pet

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
        errorcount = 0
        for x in User.objects.all():
            #check name uniqueness
            if (request.POST['username'] == x.username):
                messages.error(request, 'Username already in use.')
                errorcount += 1
            continue
        #check email format.
        if not re.match(r'^([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+)$', request.POST['email']):
            print "Error: Email is not in valid format."
            messages.error(request, 'Email is not in valid format.')
            errorcount += 1
        #check length of the password
        if (len(request.POST['password']) < 6):
                messages.error(request, 'Password must be at least 6 characters.')
                errorcount += 1
            #check if the password confirmation is a match.
        if (request.POST['password'] != request.POST['confirmpassword']):
            messages.success(request, "Password confirmtion did not match.")
            errorcount += 1
        if (errorcount > 0):
            return redirect ('/main')
        else:
            User.objects.create(username=request.POST['username'], birthdate=request.POST['birthdate'], email=request.POST['email'], password=request.POST['password'])
            messages.success(request, "Registered! You can now login and play.")
            return redirect ('/main')



def login(request):
    #check for username
    for x in User.objects.all():
        if (request.POST['username'] == x.username):
            #check password
			if (request.POST['password'] == x.password):
				request.session["username"] = User.objects.get(username=request.POST['username']).username
				request.session["id"] = User.objects.get(username=request.POST['username']).id
				return redirect("/dashboard")
			else:
				messages.error(request, "Password was incorrect.")
				return redirect("/main")
        else:
            continue
    #if not found
    messages.error(request, "Username not found")
    return redirect("/main")

def dashboard(request):
	context={
	"myanimals": Pet.objects.filter(owner=User.objects.get(id=request.session['id']))
	}
	return render(request,"dashboard.html",context)

def logout(request):
    request.session.flush()
    return redirect('/main')

def newpet(request):
	#verify the number of pets
	if(len(Pet.objects.filter(owner=User.objects.get(id=request.session['id']))) > 3):
		messages.error(request, "You have too many pets. You must get rid of one before you get another...")
		return redirect("/dashboard")
	else:
		return render(request,"newpet.html")

def addpet(request):
	#verify the number of pets incase user tries to hack the game by going to this page.
	if(len(Pet.objects.filter(owner=User.objects.get(id=request.session['id']))) > 3):
		messages.error(request, "Hey, cheater...you need to kill one of your pets first!")
		return redirect("/dashboard")
    #verify the name
	if (len(request.POST['name']) < 1):
		messages.error(request, "Please enter a name for your pet.")
		return redirect("/newpet")
	else:
	#create the pet
		randhp = random.randrange(1,30)
		Pet.objects.create(name=request.POST['name'], owner=User.objects.get(id=request.session['id']), type=request.POST['type'], maxhp=randhp, currenthp=randhp)
		return redirect("/dashboard")
	
def eatconfirm(request):
	phrases = ["No, Mommy, don't eat me!", "Go ahead, my life is miserable anyway...", "Can I have one last apple first?", "Uwaaaaaaaaaaaaaaaaaagh!", "$%@$#$%^$ You! Why would you even consider eating me!??", "But I loveded you...", "*sniff*...Okay. I'll make the sacrifice for the happiness of my family."]
	context = {
	"thispet" : Pet.objects.get(id = request.POST['id']),
	"randphrase" : phrases[random.randrange(0,len(phrases))]
	}
	return render(request,"confirmeat.html",context)

def eat(request):
		killme = Pet.objects.get(id=request.POST['id'])
		killme.delete()
		return redirect("/dashboard")
