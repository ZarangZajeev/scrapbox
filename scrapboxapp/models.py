from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    address=models.CharField(max_length=200)
    phone=models.CharField(max_length=200)
    profile_pic=models.ImageField(upload_to="profilepic",null=True,blank=True)

    def __str__(self):
        return self.user.username
    
class Category(models.Model):
    name=models.CharField(max_length=200)

class Scrap(models.Model):
    name=models.CharField(max_length=200)
    category=models.ForeignKey(Category)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_scrap")
    price=models.PositiveIntegerField()
    description=models.CharField(max_length=200)
    location=models.CharField(max_length=200)
    scrap_image=models.ImageField(upload_to="scrappics",)
    condition=models.CharField(max_length=200)
    created_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Wishlist(models.Model):
    scrap=models.ManyToManyField(Scrap,related_name="wished_scrap")
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_wish")
    created_date=models.DateTimeField(auto_now_add=True)

class Bids(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_bids")
    scrap=models.ForeignKey(Scrap)
    amount=models.PositiveIntegerField()
    status=models.CharField(max_length=200)

    def __str__(self):
        return self.amount
    
class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_review")
    scrap=models.ForeignKey(Scrap,related_name="scrap_review")
    comment=models.CharField(max_length=200)
    rating=models.CharField(max_length=200)

    def __str__(self):
        return self.comment