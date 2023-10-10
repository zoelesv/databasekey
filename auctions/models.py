from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class Customers(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
# user model for auction listings
class Listing(models.Model):
    owner = models.ForeignKey(Customers,on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.IntegerField()
    category = models.CharField(max_length=64)
    link = models.CharField(max_length=256, default=None, blank=True, null=True)
    time = models.CharField(max_length=64)

# user model for bids can use foreign key models.ForeignKey(Customers,on_delete=models.CASCADE,)
class Bid(models.Model):
    user = models.ForeignKey(Customers,on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    listingid = models.IntegerField()
    bid = models.IntegerField()

# user model for comments made on auction listings.
class Comment(models.Model):
    user = models.ForeignKey(Customers,on_delete=models.CASCADE)
    time = models.CharField(max_length=64)
    comment = models.TextField()
    listingid = models.IntegerField()

class Watchlist(models.Model):
    user = models.ForeignKey(Customers,on_delete=models.CASCADE)
    listingid = models.IntegerField()

class Closedbid(models.Model):
    owner = models.ForeignKey(Customers,on_delete=models.CASCADE)
    winner = models.CharField(max_length=64)
    listingid = models.IntegerField()
    winprice = models.IntegerField()

class Alllisting(models.Model):
    listingid = models.IntegerField()
    title = models.CharField(max_length=64)
    description = models.TextField()
    link = models.CharField(max_length=64,default=None,blank=True,null=True)
