from django.urls import reverse
from django.db.models import Max
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from .models import User, Category, BidListing, Bid, Comment


def index(request):
    obj = BidListing.objects.filter(active=True)
    return render(request, "bids/index.html", {
        "objects": obj
    })


def all(request):
    obj = BidListing.objects.all()
    return render(request, "bids/index.html", {
        "objects": obj
    })


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
            return render(request, "bids/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "bids/login.html")


@login_required
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
            return render(request, "bids/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "bids/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "bids/register.html")


@login_required
def createListing(request):
    if request.method == 'POST':
        title = request.POST["title"]
        description = request.POST["description"]
        startBid = request.POST["startBid"]
        category = Category.objects.get(id=request.POST["category"])
        user = request.user
        imageUrl = request.POST["url"]
        if imageUrl == '':
            imageUrl = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/300px-No_image_available.svg.png"
        listing = BidListing.objects.create(
            name=title, category=category, date=timezone.now(), startBid=startBid, description=description, user=user, imageUrl=imageUrl, active=True)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "bids/createListing.html", {
        'categories': Category.objects.all()
    })


def details(request, id):
    item = BidListing.objects.get(id=id)
    bids = Bid.objects.filter(bidListing=item)
    comments = Comment.objects.filter(bidListing=item)
    value = bids.aggregate(Max('bidValue'))['bidValue__max']
    bid = None
    if value is not None:
        bid = Bid.objects.filter(bidValue=value)[0]
    return render(request, "bids/details.html", {
        'item': item,
        'bids': bids,
        'comments': comments,
        'bid': bid
    })


def categories(request):
    if request.method == 'POST':
        category = request.POST["category"]
        new_category, created = Category.objects.get_or_create(
            name=category.lower())
        if created:
            new_category.save()
        else:
            messages.warning(request, "Category already Exists!")
        return HttpResponseRedirect(reverse("categories"))
    return render(request, "bids/categories.html", {
        'categories': Category.objects.all()
    })


def filter(request, name):
    category = Category.objects.get(name=name)
    obj = BidListing.objects.filter(category=category)
    return render(request, "bids/index.html", {
        "objects": obj
    })


@login_required
def comment(request, id):
    if request.method == 'POST':
        bidListing = BidListing.objects.get(id=id)
        user = request.user
        commentValue = request.POST["content"].strip()
        if(commentValue != ""):
            comment = Comment.objects.create(date=timezone.now(
            ), user=user, bidListing=bidListing, commentValue=commentValue)
            comment.save()
        return HttpResponseRedirect(reverse("details", kwargs={'id': id}))
    return HttpResponseRedirect(reverse("index"))


@login_required
def bid(request, id):
    if request.method == 'POST':
        bidListing = BidListing.objects.get(id=id)
        bidValue = request.POST["bid"]
        args = Bid.objects.filter(bidListing=bidListing)
        value = args.aggregate(Max('bidValue'))['bidValue__max']
        if value is None:
            value = 0
        if float(bidValue) < bidListing.startBid or float(bidValue) <= value:
            messages.warning(
                request, f'Bid Higher than: {max(value, bidListing.startBid)}!')
            return HttpResponseRedirect(reverse("details", kwargs={'id': id}))
        user = request.user
        bid = Bid.objects.create(
            date=timezone.now(), user=user, bidValue=bidValue, bidListing=bidListing)
        bid.save()
    return HttpResponseRedirect(reverse("details", kwargs={'id': id}))


@login_required
def end(request, itemId):
    bidListing = BidListing.objects.get(id=itemId)
    user = request.user
    if bidListing.user == user:
        bidListing.active = False
        bidListing.save()
        messages.success(
            request, f'Bid for {bidListing.name} successfully closed!')
    else:
        messages.info(
            request, 'You are not authorized to end this listing!')
    return HttpResponseRedirect(reverse("details", kwargs={'id': itemId}))


@login_required
def watchlist(request):
    if request.method == 'POST':
        user = request.user
        bidListing = BidListing.objects.get(id=request.POST["item"])
        if request.POST["status"] == '1':
            user.watchlist.add(bidListing)
        else:
            user.watchlist.remove(bidListing)
        user.save()
        return HttpResponseRedirect(
            reverse("details", kwargs={'id': bidListing.id}))
    return HttpResponseRedirect(reverse("index"))


@login_required
def watch(request):
    user = request.user
    obj = user.watchlist.all()
    return render(request, "bids/index.html", {
        "objects": obj
    })
