from email.policy import default
from pyexpat import model

from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass

class category(models.Model):
    catename = models.CharField(max_length=40)

    def __str__(self):
        return self.catename
    
class Bid(models.Model):
    bid = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True, null= True, related_name='userbid')
 
    
    

class listing(models.Model):
    title = models.CharField(max_length=20)
    Description = models.CharField(max_length=100)
    imange_url = models.CharField(max_length=1000)
    price =models.ForeignKey(Bid, on_delete=models.CASCADE , blank=True, null= True, related_name="bidprice")
    owner = models.ForeignKey(User, on_delete=models.CASCADE , blank=True, null= True, related_name='user')
    category = models.ForeignKey(category, on_delete=models.CASCADE, blank=True, null=True, related_name='category')
    isActive = models.BooleanField(default=True)
    watch_list = models.ManyToManyField(User, blank=True, null=True, related_name="listingForwatch")

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE , blank=True, null= True, related_name='usercoment')
    listing = models.ForeignKey(listing, on_delete=models.CASCADE , blank=True, null= True, related_name='listingcoment')
    massage = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.author} comment on {self.listing}"


