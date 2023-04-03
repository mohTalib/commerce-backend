from ast import arg
from inspect import ArgSpec
from turtle import title, update
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import  User, listing, category, Comment, Bid


def index(request):
    active_li= listing.objects.filter(isActive=True)
    allcatecories = category.objects.all()
    return render(request, "auctions/index.html",{
        "listings" : active_li,
        "categories": allcatecories,
    })

def Listing(request, id):
    listData1=listing.objects.get(pk=id)
    isListingInWatch_list = request.user in  listData1.watch_list.all()
    allcoment = Comment.object.all(listing=listData1)
    isOwner = request.user.username == isListingInWatch_list
    return render(request, "auctions/Listing.html", {
        "Listing": listData1,
        "isListingInWatch_list": isListingInWatch_list,
        "allcoment":allcoment,
        "isOwner":isOwner,
        "update" : True,
        "massage" : "Well Done"
    })

def addbid(request, id):
    newbid =request.POST['newbid']
    listData1 =listing.objects.get(pk=id)
    isListingInWatch_list = request.user in  listData1.watch_list.all()
    allcoment = Comment.object.all(listing=listData1)
    isOwner= request.user.username == listData1.owner.username
    if int (newbid) > listData1.price.bid:
        updateBid = Bid(user=request.user, bid=int (newbid))
        updateBid.save()
        listData1.price = updateBid
        listData1.save()
        return render(request, 'auctions/Listing.html', {
        "Listing" : listData1,
        "massage" : "Bid was updated succuessfully",
        "update": True,
        "isListingInWatch_list": isListingInWatch_list,
        "allcoment":allcoment,
        "isOwner" : isOwner,
     
        })
    else:
        return render(request, 'auctions/Listing.html', {
        "Listing" : listData1,
        "massage" : "Bid was updated Failed",
        "update": False,
        "isListingInWatch_list": isListingInWatch_list,
        "allcoment":allcoment,
        "isOwner":isOwner,

    })

def closeauic(request, id):
    listData1=listing.objects.get(pk=id)
    listData1.isActive =False
    listData1.save()
    isListingInWatch_list = request.user in  listData1.watch_list.all()
    allcoment = Comment.object.all(listing=listData1)
    isOwner= request.user.username == listData1.owner.username
    return render(request, 'auctions/Listing.html', {
        "Listing" : listData1,
        "massage" : "congragulations",
        "update": True,
        "isListingInWatch_list": isListingInWatch_list,
        "allcoment":allcoment,
        "isOwner" : isOwner,

    })
    

def displaywatch(request):
    theUser = request.user
    listings = theUser.listingForwatch.all()
    return render(request, "auctions/displaywatch.html", {
        "listings" : listings
    })

def Addtowhatchlist(request, id):
    listData1=listing.objects.get(pk=id)
    theUser = request.user
    listData1.watch_list.add(theUser)
    return HttpResponseRedirect(reverse("Listing", args = (id, )))

def Removefromwhatchlist(request, id):
    listData1=listing.objects.get(pk=id)
    theUser = request.user
    listData1.watch_list.remove(theUser)
    return HttpResponseRedirect(reverse("Listing", args = (id, )))

def addcomment(request, id):
    listData1=listing.objects.get(pk=id)
    theUser = request.user
    massage = request.POST['newcomment']
    
    newcomment = Comment(
        auther = theUser,
        listing = listData1,
        massage =massage,
    ) 

    newcomment.save()

    return HttpResponseRedirect(reverse("Listing", args = (id, )))

def displaycate(request):
     if request.method =='POST':
        categoryFormForm = request.POST['category']
        category1 = category.objects.get(catename=categoryFormForm)
     active_li= listing.objects.filter(isActive=True, category=category1)
     allcatecories = category.objects.all()
     return render(request, "auctions/index.html",{
        "listings" : active_li,
        "categories": allcatecories,
    })
    

def createlist(request):
    if request.method == 'GET':
        allcatecories = category.objects.all()
        return render(request, 'auctions/list.html', {
        "categories" : allcatecories
    
        })
    else:
            title = request.POST["title"]
            description = request.POST["Description"]
            imageurl = request.POST["imageurl"]
            price = request.POST["price"]
            Category = request.POST["category"]
            theUser = request.user
            category_cont = Category.objects.get(catename=Category)
            bid = Bid(bid=int(price), user = theUser)
            bid.save()
            newlist = listing(
                title=title,
                Description=description,
                imange_url=imageurl,
                price=bid,
                category=category_cont,
                owner= theUser,
            )
            newlist.save()
            return HttpResponseRedirect(reverse(index))
   
             

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
