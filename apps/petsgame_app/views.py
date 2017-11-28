# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
import datetime
import re, random
from random import randint
from models import User, Pet, Item

item = {"monkey": "A cheeky monkey dropped from the trees and stole some items!","secret":["peggy","draggy"],"bear":"Oh no! A bear attacked! Everyone lost 6HP.", "forest fire":"Uh, oh...a forest fire started. It did some serious damage before you could escape...", "mushroom":"It looks safe...", "water":"Refreshing, hydrating!", "honey":"Delicious bee vomit. Good for humans.", "bug":"Good source of protein.", "berry":"So sweet! Pets love this.", "apple":"Tasty fruit. This is people food!","stick":"A solid twig, easy to hold.", "flower":"Makes all your pets happier.", "acorn":"A dry, icky nut."}
	
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
		return redirect ('/')
	else:
		myhealth = randint(50,101)
		User.objects.create(username=request.POST['username'], birthdate=request.POST['birthdate'], email=request.POST['email'], password=request.POST['password'], health=myhealth, maxhealth=myhealth)
		messages.success(request, "Registered! You can now login and play.")
		return redirect ('/')

def login(request):
    #check for username
    for x in User.objects.all():
        if (request.POST['username'] == x.username):
            #check password
			if (request.POST['password'] == x.password):
				request.session["username"] = User.objects.get(username=request.POST['username']).username
				request.session["id"] = User.objects.get(username=request.POST['username']).id
				print "User login reached."
				return redirect("/dashboard")
			else:
				messages.error(request, "Password was incorrect.")
				return redirect("/")
        else:
            continue
    #if not found
    messages.error(request, "Username not found")
    return redirect("/")

def dashboard(request):
	context={
	"myanimals": Pet.objects.filter(owner=User.objects.get(id=request.session['id'])),
	"today": datetime.date.today(),
	"myitems": Item.objects.filter(owner=User.objects.get(id=request.session['id'])),
	"player": User.objects.get(id=request.session['id']),
	}
	myanimals = Pet.objects.filter(owner=User.objects.get(id=request.session['id']))
	myitems = Item.objects.filter(owner=User.objects.get(id=request.session['id']))
	player = User.objects.get(id=request.session['id'])
	today = datetime.date.today()
	
	#if player's pet dies, is hungry, or maxes out HP
	for x in myanimals:
		if (x.currenthp <= 0):
			myname = x.name
			messages.error(request, "Uh, oh..." + myname + " died.")
			x.delete() 
		elif (x.currenthp <= 2):
			messages.error(request, x.name + " is really weak and hungry. Better feed them something quickly!")
		elif (x.currenthp > x.maxhp):
			x.currenthp = x.maxhp
			x.save()
			messages.error(request, x.name + " is already at max HP. Perhaps using an item could increase it...")
		
	#if player is out of items
	for x in myitems:
		if (x.amount <= 0):
			messages.error(request, "You are all out of " + x.item)
			x.delete()
			
	#if player is dead, or maxes out their hp
	if (player.health <= 0):
		for x in myanimals:
			x.owner = None
			x.save()
		return render(request, "death.html", context)
	elif (player.health > player.maxhealth):
		player.health = player.maxhealth
		player.save()
		messages.error(request, "You have reached your max health...perhaps an item can increase it?")
		
		
	return render(request,"dashboard.html", context)
	
def death(request):
	myhealth = random.randrange(50,101)
	player = User.objects.get(id=request.session['id'])
	
	player.health = myhealth
	player.save()
	player.maxhealth = myhealth
	player.save()
	return redirect("/dashboard")

def logout(request):
    request.session.flush()
    return redirect('/')

def help(request):
	return render(request, "help.html")
	

	
#CREATE A NEW PET
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
		messages.error(request, "Hey, cheater...you can't have more than 3 pets!")
		return redirect("/dashboard")
    #verify the name
	if (len(request.POST['name']) < 1):
		messages.error(request, "Please enter a name for your pet.")
		return redirect("/newpet")
	else:
	#create the pet
		randhp = random.randrange(10,31)
		Pet.objects.create(name=request.POST['name'], owner=User.objects.get(id=request.session['id']), type=request.POST['type'], maxhp=randhp, currenthp=randhp)
		return redirect("/dashboard")
		
#EAT A PET	
def eatconfirm(request):
	phrases = ["No, Mommy, don't eat me!", "Go ahead, my life is miserable anyway...", "Can I have one last apple first?", "Uwaaaaaaaaaaaaaaaaaagh!", "$%@$#$%^$ You! Why would you even consider eating me!??", "But I loveded you...", "*sniff*...Okay. I'll make the sacrifice for the happiness of my family."]
	context = {
	"thispet" : Pet.objects.get(id = request.POST['id']),
	"randphrase" : phrases[random.randrange(0,len(phrases))]
	}
	return render(request,"confirmeat.html",context)

def eat(request):
	killme = Pet.objects.get(id=request.POST['id'])
	userpets = Pet.objects.filter(owner=User.objects.get(id=request.session['id']))
	player = User.objects.get(id=request.session["id"])
	for x in userpets:
		x.currenthp += 10;
		x.save();
	player.health += 10
	player.save()
	deadname = killme.name;
	messages.success(request,"You feasted on " + deadname + "'s carcass with your pets, and everyone gained 10 HP!")			
	killme.delete()
	return redirect("/dashboard")
		
#HUNT FEATURE
def hunt(request):
	pass
		
#FORAGE FOR ITEMS		
def forage(request):
	forageitem = item.keys()[random.randrange(0,len(item))]
	mypets = Pet.objects.filter(owner=User.objects.get(id=request.session['id']))
	player = User.objects.get(id=request.session['id'])
	myitems = Item.objects.filter(owner=request.session['id'])
	
	#If you find a secret pet
	if (forageitem == "secret"):
		thesecret = item["secret"][random.randrange(0,len(item["secret"]))]
		context = {
			"secretpet": thesecret,
		}
		return render(request,"secretpet.html", context)
		
	#These are the special events
	if (forageitem == "bear"):
		messages.error(request, item['bear'])
		for x in mypets:
			x.currenthp = x.currenthp -6
			x.save()
		player.health -= 6
		player.save()
		return redirect('/dashboard')
	
	if (forageitem == "forest fire"):
		messages.error(request, item['forest fire'])
		for x in mypets:
			x.currenthp -= 25
			x.save()
		player.health -= 25
		player.save()
		return redirect('/dashboard')
	
	if (forageitem == "monkey"):
		messages.error(request, item['monkey'])
		stolen = myitems[random.randrange(0,len(myitems))]
		stolen.delete()
		return redirect('/dashboard')
		
	#If it is an item...
	if (myitems):
		for x in myitems:
			if (x.item == forageitem):
				x.amount = x.amount + 1
				x.save()
				messages.success(request, "You found a " + forageitem +".")
				return redirect("/dashboard")
			else:
				continue
	Item.objects.create(item=forageitem, owner=player, amount=1)
	messages.success(request, "You found a " + forageitem +".")
	return redirect("/dashboard")
				
#ITEM EFFECTS AND USE		
def useitem(request):
		#all the current user's items as a list of objects
		
		thisitem = Item.objects.get(owner=User.objects.get(id=request.session['id']), item=request.POST['item'])
		mypets = Pet.objects.filter(owner=User.objects.get(id=request.session['id']))
		player = User.objects.get(id = request.session['id'])
		myitems = Item.objects.filter(owner=request.session['id'])
		
		if (request.POST['item'] == 'apple'):
			player.health += 5
			player.save()
			thisitem.amount -= 1
			thisitem.save()
			messages.success(request, "You ate the juicy, crisp apple and gained 5 health points.")
			return redirect ('/dashboard')
			
		if (request.POST['item'] == 'stick'):
			mypets = Pet.objects.filter(owner=User.objects.get(id = request.session['id']))
			thispet = mypets[random.randrange(0,len(mypets))]
			thispet.currenthp = thispet.currenthp - 3
			thispet.save()
			thisitem.amount -= 1
			thisitem.save()
			messages.success(request, "You threw the stick and it bopped " + thispet.name + " on the head. Ouch!")
			return redirect("/dashboard")
				
				
		if (request.POST['item'] == 'berry'):
			randpet = mypets[random.randrange(0,len(mypets))]
			randpet.currenthp += 1
			randpet.maxhp += 1
			randpet.save()
			thisitem.amount -= 1
			thisitem.save()
			messages.success(request, randpet.name + " ate the berry from your hand and gained 1HP and +1 max HP!")
			return redirect("/dashboard")
			
		if (request.POST['item'] == 'mushroom'):
			thispet = mypets[random.randrange(0,len(mypets))]
			effects = ["goodshroom", "badshroom"]
			effect = effects[random.randrange(0, len(effects))]
			if (effect == "badshroom"):
				if (thispet.currenthp < 1):
					pass
					messages.success(request, thispet.name + " was brave (or hungry) enough to eat the mushroom. Nothing happened.")
					thisitem.amount -= 1
					thisitem.save()
					return redirect("/dashboard")
					
				else:
					thispet.currenthp -= 2
					thispet.save()
					messages.success(request, thispet.name + " was brave (or hungry) enough to eat the mushroom. Oops...HP-2.")
					thisitem.amount -= 1
					thisitem.save()
					return redirect("/dashboard")
				
			if (effect == "goodshroom"):
				if (thispet.currenthp < thispet.maxhp):
					thispet.currenthp += 2
					thispet.save()
					messages.success(request, thispet.name + " was brave (or hungry) enough to eat the mushroom...HP + 2!")
					thisitem.amount -= 1
					thisitem.save()
					return redirect("/dashboard")
				else:
					messages.success(request, thispet.name + " was brave (or hungry) enough to eat the mushroom. Nothing happened.")
					thisitem.amount -= 1
					thisitem.save()
					return redirect("/dashboard")
	
		if (request.POST['item'] == 'water'):
			for x in mypets:
				x.currenthp += 2
				x.save()
			player.health += 2
			player.save()
			thisitem.amount = thisitem.amount -1
			thisitem.save()
			if (thisitem.amount < 1):
				thisitem.delete()
			messages.success(request, "You shared the water with all of your pets.")
			return redirect("/dashboard")
			
		if (request.POST['item'] == 'honey'):
			player.maxhealth += 3
			player.save()
			thisitem.amount -= 1
			thisitem.save()
			if (thisitem.amount < 1):
				thisitem.delete()
			messages.success(request, "You gained a boost of stamina from the honey. +3 max HP!")
			return redirect("/dashboard")
			
		if (request.POST['item'] == 'acorn'):
			randpet = mypets[random.randrange(0, len(mypets))]
			randpet.currenthp += 5
			randpet.save()
			thisitem.amount = thisitem.amount -1
			thisitem.save()
			if (thisitem.amount < 1):
				thisitem.delete()
			messages.success(request, randpet.name + " ate the acorn and gained 5 HP!")
			return redirect("/dashboard")
				
			
		if (request.POST['item'] == 'bug'):
			thisitem.amount = thisitem.amount -1
			thisitem.save()
			if (thisitem.amount < 1):
				thisitem.delete()
			who = [player]
			for x in mypets:
				who.append(x)
			me = who[random.randrange(0,len(who))]
			if (me == player):
				player.health += 5
				player.save()
				messages.success(request, "You decided to eat the bug and gained 5 health.")
				return redirect("/dashboard")
			else:	
				me.currenthp += 5
				me.save()
				messages.success(request, me.name + " ate the bug and gained 5HP.")
				return redirect("/dashboard")
			
		if (request.POST['item'] == 'flower'):
			for x in Pet.objects.filter(owner=User.objects.get(id = request.session['id'])):
				if (x.currenthp < x.maxhp):
					x.currenthp = x.currenthp + 1
					x.save()
				else:
					continue
			thisitem.amount = thisitem.amount -1
			thisitem.save()
			if (thisitem.amount < 1):
				thisitem.delete()
			messages.success(request, "You waved the flower around in front of your pets. Their eyes light up and they gained a little health.")
			return redirect("/dashboard")
			
def catchsecret(request):
	player = User.objects.get(id = request.session["id"])
	secretpet = request.POST["secretpet"]
	name = request.POST["name"]
	chance = [0,0,1,1,1,2]
	catch = chance[random.randrange(0,len(chance))]
	if (catch == 0):
		messages.error(request, "You tried to approach the " + secretpet + ", but it ran away. Maybe you smelled funny.")
		return redirect("/dashboard")
	elif (catch == 2):
		messages.error(request, "You tried to approach the " + secretpet + "gently, but it felt threatened and attacked you!")
		player.health -= 10
		player.save()
		return redirect("/dashboard")
	elif (catch == 1):
		hp = random.randrange(100,201)
		messages.success(request, "You approached the " + secretpet + " and it licked your face affectionately, and followed you out of the woods.")
		Pet.objects.create(name=name, type=secretpet, currenthp=hp, maxhp=hp, owner=player)
		return redirect("/dashboard")

#HUNT FEATURE
def hunt(request):
	myanimals = Pet.objects.filter(owner=User.objects.get(id=request.session['id']))
	myitems = Item.objects.filter(owner=User.objects.get(id=request.session['id']))
	player = User.objects.get(id=request.session['id'])
	otheranimals = Pet.objects.exclude(owner=User.objects.get(id=request.session['id']))
	try:
		opponent = otheranimals[random.randrange(0, len(otheranimals))]
	except ValueError:
		messages.error(request, "The forest is silent...")
		return redirect('/dashboard')
	attacker = myanimals[random.randrange(0, len(myanimals))]
	context = {
		"attacker": attacker,
		"opponent": opponent,
	}
	if (opponent.currenthp <= 0):
		opponent.delete()
		return redirect('/huntkill')
	if (attacker.currenthp <= 0):
		return redirect('/dashboard')
	return render(request, "hunt.html", context)
	
def huntkeep(request):
	pet = Pet.objects.get(id=request.POST['opponent'])
	player = User.objects.get(id=request.session['id'])
	pet.owner = player
	pet.save()
	return redirect('/dashboard')
	
def huntkill(request):
	messages.success(request, "You won the fight! You and your pets ate the poor loser and gained 10HP.")
	myanimals = Pet.objects.filter(owner=User.objects.get(id=request.session['id']))
	myitems = Item.objects.filter(owner=User.objects.get(id=request.session['id']))
	player = User.objects.get(id=request.session['id'])
	player.health += 10
	player.save()
	for x in myanimals:
		x.currenthp += 10
		x.save()
	return redirect('/dashboard')
	
def attack(request):
	attacker = Pet.objects.get(id=request.POST["attacker"])
	opponent = Pet.objects.get(id=request.POST["opponent"])
	context = {
		"attacker": request.POST["attacker"],
		"opponent": request.POST["opponent"],
	}
	power = random.randrange(1,attacker.maxhp)
	opponent.currenthp -= power
	opponent.save()
	messages.success(request, attacker.name + " attacked " + opponent.name + " for " + power + " HP!") 
	if (opponent.currenthp > 0):
		defendpow = random.randrange(1,opponent.maxhp)
		attacker.currenthp -= defendpow
		attacker.save()
		messages.success(request, opponent.name + " attacked " + attacker.name + " back for " + power + " HP!") 
	return render(request, "hunt.html", context)

		

			
		