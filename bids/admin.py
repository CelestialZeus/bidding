from django.contrib import admin
from .models import Category, BidListing, User, Comment, Bid

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(BidListing)
admin.site.register(Bid)
admin.site.register(Comment)
