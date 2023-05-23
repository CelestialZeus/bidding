from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField(
        'BidListing', blank=True, related_name="userWatchlist")


class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.id} : {self.name}"


class BidListing(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date = models.DateTimeField()
    startBid = models.DecimalField(decimal_places=2, max_digits=7)
    description = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imageUrl = models.URLField(blank=True)
    active = models.BooleanField()

    def __str__(self):
        return f"{self.id} : {self.name} in {self.category.name}\nPosted at : {self.date}\nValue : {self.startBid}\nDescription : {self.description}\nPosted By : {self.user.username} Active Status: {self.active}"


class Bid(models.Model):
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bidValue = models.DecimalField(decimal_places=2, max_digits=7)
    bidListing = models.ForeignKey(
        BidListing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} : {self.user.username} bid {self.bidValue} on {self.bidListing.name} at {self.date}"


class Comment(models.Model):
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bidListing = models.ForeignKey(
        BidListing, on_delete=models.CASCADE)
    commentValue = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.id} : {self.user.username} commented on {self.bidListing.name} posted by {self.bidListing.user.username} at {self.date} : {self.commentValue}"
