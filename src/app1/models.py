from django.db import models
from django.contrib import admin
from datetime import datetime
from django_countries.fields import CountryField

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
    start_date = models.DateField(null=True, blank = True)
    end_date = models.DateField(null=True, blank = True)
    day = models.CharField(max_length=20, blank = True)
    hour = models.CharField(max_length=20, blank = True)

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
    start_date = models.DateField(null=True, blank = True)
    end_date = models.DateField(null=True, blank = True)
    day = models.CharField(max_length=20, blank = True)
    hour = models.CharField(max_length=20, blank = True)
    

class Rating_Review(models.Model) :
    senior_email = models.CharField(max_length=200)
    caregiver_email = models.CharField(max_length=200)
    rating=models.IntegerField(default=0)
    review=models.TextField(max_length=1024, blank = True)

class Posts(models.Model) :
    created_by = models.CharField(max_length=200)
    created_at = models.DateField(default=datetime.now())
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by_name = models.CharField(max_length=2048, null=True, blank=True)

class Comments(models.Model) :
    post_id = models.ForeignKey(Posts, on_delete = models.CASCADE)
    created_by = models.CharField(max_length=200)
    created_at = models.DateField(default=datetime.now())
    content = models.TextField()
    created_by_name = models.CharField(max_length=2048, null=True, blank=True)

class Room(models.Model) :
    ''' Represents chat rooms that users can join '''
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    slug = models.CharField(max_length=50)

    def __str__(self) :
        '''  Returns human-readable representation of the model instance  '''
        return self.name

class UserChats(models.Model) :
    #User will be a concatenation of user type and user id
    user = models.CharField(max_length=255)
    chat_slug = models.CharField(max_length=50)
    with_user = models.CharField(max_length=255, default = "")


class Address(models.Model):
    # name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    # address_type = models.CharField(max_length=1, type=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

class Transaction(models.Model):
    senior_email = models.CharField(max_length=200)
    caregiver_email = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    start_date= models.DateField(null=True, blank = True)
    end_date=models.DateField(null=True, blank = True)
    number_of_days = models.IntegerField(null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    availability = models.CharField(max_length = 25, null=True, blank=True)
    paid = models.BooleanField(null=True, blank=True, default='False')

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    email = models.CharField(max_length=200)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Match(models.Model) :
    senior_email = models.CharField(max_length=200)
    caregiver_email = models.CharField(max_length=200)

# class UserProfile(models.Model):
#     email = models.CharField(max_length=50)
#     stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
#     one_click_purchasing = models.BooleanField(default=False)

#     def __str__(self):
#         return self.email

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
admin.site.register(Room)
admin.site.register(UserChats)
admin.site.register(Address)
admin.site.register(Match)
admin.site.register(Rating_Review)
admin.site.register(Transaction)
