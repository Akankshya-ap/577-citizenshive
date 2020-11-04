from django.db import models
from django.contrib import admin
from datetime import datetime

# Create your models here.

class CommonRegistration(models.Model) :
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    userType = models.CharField(max_length=25)

class Senior(models.Model) :
    email = models.CharField(max_length=200)
    name = models.CharField(max_length=200, blank = True)
    password = models.CharField(max_length=200)
    dob = models.DateField(null=True, blank = True)
    availability = models.CharField(max_length=25, blank = True)
    zip_code = models.CharField(max_length=20, blank = True)
    city = models.CharField(max_length=25, blank = True)
    state = models.CharField(max_length=25,blank = True)
    bio = models.TextField(max_length=1024, blank = True)
    profile_image = models.ImageField(upload_to='images/', blank = True, default = 'images/person_avatar.png')

class Caregiver(models.Model) :
    email = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    dob = models.DateField(null=True, blank = True)
    availability = models.CharField(max_length=25, blank = True)
    zip_code = models.CharField(max_length=20, blank = True)
    city = models.CharField(max_length=25, blank = True)
    state = models.CharField(max_length=25,blank = True)
    bio = models.TextField(max_length=1024, blank = True)
    profile_image = models.ImageField(upload_to='images/', blank = True, default='images/person_avatar.png')

class Posts(models.Model) :
    created_by = models.CharField(max_length=200)
    created_at = models.DateField(default=datetime.now())
    title = models.CharField(max_length=200)
    content = models.TextField()

class Comments(models.Model) :
    post_id = models.ForeignKey(Posts, on_delete = models.CASCADE)
    created_by = models.CharField(max_length=200)
    created_at = models.DateField(default=datetime.now())
    content = models.TextField()

class Match(models.Model) :
    senior_email = models.CharField(max_length=200)
    caregiver_email = models.CharField(max_length=200)

# # Create your models here.
# class Product(models.Model): 
#     title  = models.CharField(max_length=120)  
#     description = models.TextField(blank=True)
#     price = models.DecimalField(decimal_places=2, max_digits=1000)
#     summary = models.TextField(blank=False, null=False)
#     featured = models.BooleanField(default=True) #null = True, default = True


admin.site.register(CommonRegistration)
admin.site.register(Senior)
admin.site.register(Caregiver)
admin.site.register(Posts)
admin.site.register(Comments)
admin.site.register(Match)