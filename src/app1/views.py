from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from .models import CommonRegistration, Senior, Caregiver, Posts, Comments, Room, UserChats, Address, Match
import json
from pyzipcode import ZipCodeDatabase  
# 
import random
import string

import stripe

from django.contrib import messages
from .forms import CheckoutForm, PaymentForm
from django.views.generic import ListView, DetailView, View
# Create your views here.

from django.conf import settings
from django.http import JsonResponse


from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant
import datetime

fake = Faker()

# Create your views here.


def all_rooms(request) :
    rooms = Room.objects.all()
    return render(request, 'chat_index.html', {'rooms': rooms, 'user_type' : request.session['user_type']})


def room_detail(request, slug) :
    room = Room.objects.get(slug = slug)
    return render(request, 'chat_room_detail.html',{'room': room, 'user_type' : request.session['user_type']})

def token(request):
    # identity = request.GET.get('identity', fake.user_name())
    if request.session['user_type'] == 'senior' :
        user_obj = Senior.objects.get(email = request.session['email'])
    else :
        user_obj = Caregiver.objects.get(email = request.session['email'])
    identity = user_obj.name
    device_id = request.GET.get('device', 'default')  # unique device ID

    account_sid = settings.TWILIO_ACCOUNT_SID
    api_key = settings.TWILIO_API_KEY
    api_secret = settings.TWILIO_API_SECRET
    chat_service_sid = settings.TWILIO_CHAT_SERVICE_SID

    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Create a unique endpoint ID for the device
    endpoint = "MyDjangoChatRoom:{0}:{1}".format(identity, device_id)

    if chat_service_sid:
        chat_grant = ChatGrant(endpoint_id=endpoint,
                               service_sid=chat_service_sid)
        token.add_grant(chat_grant)

    response = {
        'identity': identity,
        'token': token.to_jwt().decode('utf-8')
    }

    return JsonResponse(response)


def add_or_get_chatroom(request, user_id) :

    
    if request.session['user_type'] == 'senior' :
        # If it is a senior requesting to chat to a caregiver
        senior_obj = Senior.objects.get(email = request.session['email'])
        caregiver_obj = Caregiver.objects.get(id = user_id)
        user1_name = senior_obj.name
        user2_name = caregiver_obj.name
        senior_id = senior_obj.id
        caregiver_id = user_id
        chatroom_slug = 'senior_' + str(senior_id) + '_caregiver_' + str(caregiver_id)
    else :
        # If it is a caregiver requesting to chat to a senior
        caregiver_obj = Caregiver.objects.get(email = request.session['email'])
        senior_obj = Senior.objects.get(id = user_id)
        user1_name = caregiver_obj.name
        user2_name = senior_obj.name
        caregiver_id = caregiver_obj.id
        senior_id = user_id
        chatroom_slug = 'senior_' + str(senior_id) + '_caregiver_' + str(caregiver_id)
        pass

    rooms = Room.objects.filter(slug = chatroom_slug)

    if len(rooms) == 0 :
        room_name = 'Chat between ' + user1_name + ' and ' + user2_name
        Room.objects.create(name=room_name, description = ' Description ', slug = chatroom_slug)
        #Add an entry to the UserChats table
        UserChats.objects.create(user = 'senior_' + str(senior_id), chat_slug=chatroom_slug, with_user=caregiver_obj.name)
        UserChats.objects.create(user = 'caregiver_' + str(caregiver_id), chat_slug=chatroom_slug, with_user=senior_obj.name)
        #Redirect to the chatroom

    else :
        # They have chatted previously so no step needed to create a chatroom
        pass

    
    return redirect('room_detail', slug = chatroom_slug)
    # return redirect('all_rooms')


def get_chats(request) :
   
    context = {}
    user_type = request.session['user_type']
    if user_type == 'senior' :
        user_obj = Senior.objects.get(email = request.session['email'])
    else :
        user_obj = Caregiver.objects.get(email = request.session['email'])
    chats = UserChats.objects.filter(user = user_type + "_" + str(user_obj.id))
    
    context['chats'] = chats
    context['user_type'] = request.session['user_type']
    return render(request, 'view_all_chats.html', context)

def logout(request, *args, **kwargs) :
    #Delete the current session variables
    del request.session['user_type']
    del request.session['email']
    del request.session['password']
    return redirect('landing_page')


def view_caregiver_details(request, caregiver_id) :
    # return HttpResponse("<h1> Hey" + str(caregiver_id) + "</h1>")
    context = {}
    caregiver_obj = Caregiver.objects.get(id=caregiver_id)
    context['caregiver'] = caregiver_obj
    context['user_type'] = request.session['user_type']
    return render(request, 'caregiver_details_for_senior.html', context)

def view_senior_details(request, senior_id) :
    context = {}
    senior_obj = Senior.objects.get(id=senior_id)
    context['caregiver'] = senior_obj
    context['user_type'] = request.session['user_type']
    return render(request, 'senior_details_for_caregiver.html', context)

def search_caregivers(request, *args, **kwargs) :
    context = {}
    context['user_type'] = request.session['user_type']
    # zcdb = ZipCodeDatabase()
    # in_radius = [z.zip for z in zcdb.get_zipcodes_around_radius('90007', 8)] # ('ZIP', radius in miles)
    # radius_utf = [x.encode('UTF-8') for x in in_radius] # unicode list to utf list
    # context['data'] = radius_utf
    # zip, gender, radius
    if request.method == 'POST' :
        zip_code = request.POST['zip']
        radius = int(request.POST['radius'])
        zcdb = ZipCodeDatabase() 
        start_date = datetime.datetime.strptime(request.POST['start_date'], "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(request.POST['end_date'], "%Y-%m-%d").date()
        availability = request.POST['availability']
        in_radius = [z.zip for z in zcdb.get_zipcodes_around_radius(zip_code, radius)] # ('ZIP', radius in miles)
        # radius_utf = [x.encode('UTF-8') for x in in_radius] # unicode list to utf list
        radius_arr = [x.encode('utf-8').decode('unicode-escape') for x in in_radius]
        # radius_arr = 10 #added 28/10
        # caregivers = Caregiver.objects.filter(zip_code__in = radius_arr)
        caregivers = Caregiver.objects.filter(zip_code__in = radius_arr, availability=availability, start_date__lte=start_date, end_date__gte=end_date)
        context['caregivers'] = caregivers
        context['isPostRequest'] = True
    else :
        context['caregivers'] = []
        context['isPostRequest'] = False
    return render(request, 'search_caregivers.html', context)

def search_seniors(request, *args, **kwargs) :
    context = {}
    context['user_type'] = request.session['user_type']
    # zcdb = ZipCodeDatabase()
    # in_radius = [z.zip for z in zcdb.get_zipcodes_around_radius('90007', 8)] # ('ZIP', radius in miles)
    # radius_utf = [x.encode('UTF-8') for x in in_radius] # unicode list to utf list
    # context['data'] = radius_utf
    # zip, gender, radius
    if request.method == 'POST' :
        zip_code = request.POST['zip']
        radius = int(request.POST['radius'])
        zcdb = ZipCodeDatabase() 
        start_date = datetime.datetime.strptime(request.POST['start_date'], "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(request.POST['end_date'], "%Y-%m-%d").date()
        availability = request.POST['availability']
        in_radius = [z.zip for z in zcdb.get_zipcodes_around_radius(zip_code, radius)] # ('ZIP', radius in miles)
        # radius_utf = [x.encode('UTF-8') for x in in_radius] # unicode list to utf list
        radius_arr = [x.encode('utf-8').decode('unicode-escape') for x in in_radius]
        # radius_arr = 10 #added 28/10
        seniors = Senior.objects.filter(zip_code__in = radius_arr,availability=availability, start_date__lte=start_date, end_date__gte=end_date)
        context['seniors'] = seniors
        context['isPostRequest'] = True
    else :
        context['seniors'] = []
        context['isPostRequest'] = False
    return render(request, 'search_seniors.html', context)


def dashboard_view(request, *args, **kwargs) :
    user_type = request.session['user_type']
    if user_type  == 'senior' :
        return redirect('senior_dashboard_view')
    else :
        return redirect('caregiver_dashboard_view')

def caregiver_dashboard_view(request, *args, **kwargs) :
    context = {}
    context['user_type'] = request.session['user_type']
    if 'email' in request.session :
        email = request.session['email']

    if request.method == 'POST' :
        # name = request.session['name']
        # email = request.session['email']
        dob = request.POST['dob']
        availability = request.POST['availability']
        zip_code = request.POST['zip']
        city = request.POST['city']
        state = request.POST['state']
        bio = request.POST['bio']
        # profile_image = request.FILES['profile_image']

        record = Caregiver.objects.get(email=email)
        record.name = record.name 
        record.availability = availability
        record.zip_code = zip_code
        record.city = city
        record.state = state
        record.bio = bio
        record.dob = dob if dob!="" else None
        # record.profile_image = profile_image

        record.save()
        context['record'] = record
        #context['profile_image_url'] = record.profile_image.url
        #context['image_object'] = record.profile_image
        return render(request, 'caregiver_dashboard.html', context)
    else :
        context['record'] = Caregiver.objects.get(email = request.session['email'])
        #context['profile_image_url'] = 'default'
        #context['image_object'] = record.profile_image
        return render(request, 'caregiver_dashboard.html', context)



def senior_dashboard_view(request, *args, **kwargs) :
    context = {}
    context['user_type'] = request.session['user_type']
    if 'email' in request.session :
        email = request.session['email']

    if request.method == 'POST' :
        # name = request.session['name']
        # email = request.session['email']
        dob = request.POST['dob']
        availability = request.POST['availability']
        zip_code = request.POST['zip']
        city = request.POST['city']
        state = request.POST['state']
        bio = request.POST['bio']
        # profile_image = request.FILES['profile_image']

        record = Senior.objects.get(email=email)
        record.name = record.name 
        record.availability = availability
        record.zip_code = zip_code
        record.city = city
        record.state = state
        record.bio = bio
        record.dob = dob if dob!="" else None
        # record.profile_image = profile_image

        record.save()
        context['record'] = record
        #context['profile_image_url'] = record.profile_image.url
        #context['image_object'] = record.profile_image
        return render(request, 'senior_dashboard.html', context)
    else :
        context['record'] = Senior.objects.get(email = request.session['email'])
        #context['profile_image_url'] = 'default'
        #context['image_object'] = record.profile_image
        return render(request, 'senior_dashboard.html', context)


def add_post_comment(request, *args, **kwargs) :
    post_id = request.GET['comment_for_postId']
    comment_content = request.GET['comment']
    print(request)
    Comments.objects.create(post_id= Posts.objects.get(id=post_id), content = comment_content)
    #return HttpResponse("<h1> Hey, you are about to add a comment for post id = " + post_id + ", with comment = " + comment_content   +  " </h1>")
    return redirect('forum')

def add_new_post(request, *args, **kwargs) :
    # return HttpResponse("<h1> Hey </h1>")
    #Add the content to posts
    Posts.objects.create(created_by=request.POST['email'], content = request.POST['content'], title = request.POST['title'])
    return redirect('forum')

def forum(request, *args, **kwargs) :
    #Get all the current posts
    posts = Posts.objects.all()
    posts_array = []
    for post in posts :
        post_details = {
            'post_id' : post.id,
            'post_created_by': post.created_by ,
            'post_created_at' : post.created_at ,
            'post_content' : post.content ,
            'post_title' : post.title ,
            'post_comments' : Comments.objects.filter(post_id = post.id)
        }
        posts_array.append(post_details)
    context = {
        'posts_array': posts_array
    }
    context['user_type'] = request.session['user_type']
    return render(request, 'forum_page.html', context)

def handle_login(request, *args, **kwargs) :
    #Check if the user exists
    email = request.POST['email']
    password = request.POST['password']
    records = CommonRegistration.objects.filter(email = email)

    if len(records) == 0 :
        return redirect('landing_page')
    else :
        # record = records.first()
        user_type = records.first().userType
        request.session['user_type'] = user_type
        request.session['email'] = email
        request.session['password'] = password
        if user_type == 'senior' :
            record = Senior.objects.get(email = email)
        else :
            record = Caregiver.objects.get(email = email)
        context = {
            'record' : record
        }
        request.session['name'] = record.name

        #Add values to the session
        # request.session['isLoggedIn']  = True
        # request.session['email'] = email
        # request.session['userType'] = user_type
        context['user_type'] = request.session['user_type']
        if user_type == 'senior' :
            return render(request, 'senior_dashboard.html', context)
        else :
            return render(request, 'caregiver_dashboard.html', context)
        


def landing_page(request, *args, **kwargs) :
    context = {}
    if 'user_type' in request.session:
        context['user_type'] = request.session['user_type']
    if 'email' in request.session :
        #The user is already logged in
        user_type = request.session['user_type']
        email = request.session['email']
        password = request.session['password']
        if user_type == 'senior' :
            context['record'] = Senior.objects.get(email = email)
        else :
            context['record'] = Caregiver.objects.get(email = email)
        
        return render(request, 'senior_dashboard.html', context)
    else :
        return render(request, 'landing_page.html', context)

def registration_page(request, *args, **kwargs) :
    # return HttpResponse("<h1> Hello Mugdha </h1>")
    context = {}
    context['user_type'] = request.session['user_type']
    if request.method == 'POST' :
        # return HttpResponse("<h1> Response Received </h1>")
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['psw']
        user_type = request.POST['optradio']

        record_exists = CommonRegistration.objects.filter(email = email).count() > 0

        if record_exists :
            context['error_msg'] = 'This user exists already'
            return render(request, 'registration_page.html', context)
        else :
            common_registration_obj = CommonRegistration.objects.create(email=email, password=password, userType=user_type)

            if user_type == 'senior' :
                senior_obj = Senior.objects.create(name=name, email=email, password=password)
            else :
                caregiver_obj = Caregiver.objects.create(name=name, email=email, password=password)
            # return render(request, 'login_page.html', {})
            return redirect('landing_page')


    else :
        return render(request, 'registration_page.html', context)
    
def about_us(request, *args, **kwargs):
    context = {}
    context['user_type'] = request.session['user_type']
    return render(request, 'about_us.html', context)

def order_summary(request, *args, **kwargs):
    try:
        context = {
            
        }
        context['user_type'] = request.session['user_type']
        return render(request, 'order_summary.html', context)
    except ObjectDoesNotExist:
        messages.warning(request, "You do not have an active order")
        context['user_type'] = request.session['user_type']
        return render(request, 'order_summary.html', context)


def services(request, *args, **kwargs):
    context = {}
    try:
        context['user_type'] = request.session['user_type']

    except: 
        context = {}
    return render(request, 'services.html', context)

def contact(request, *args, **kwargs):
    context = {}
    try:
        context['user_type'] = request.session['user_type']

    except: 
        context = {}
    return render(request, 'contact.html', context)

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            form = CheckoutForm()
            context = {
                'form': form,
            }

            billing_address_qs = Address.objects.filter(
                email=self.request.session['email'],
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            # order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')

                if use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        email=self.request.session['email'],
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        # order.billing_address = billing_address
                        # order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_country = form.cleaned_data.get(
                        'billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_country, billing_zip]):
                        billing_address = Address(
                            email=self.request.session['email'],
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            country=billing_country,
                            zip=billing_zip,
                        )
                        billing_address.save()

                        # order.billing_address = billing_address
                        # order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required billing address fields")
                        return redirect('checkout')

                # payment_option = form.cleaned_data.get('payment_option')

                # if payment_option == 'S':
                return redirect('payment') #, payment_option='stripe')
                # elif payment_option == 'P':
                #     return redirect('core:payment', payment_option='paypal')
                # else:
                messages.warning(
                    self.request, "Invalid payment option selected")
                return redirect('checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("order_summary")



class PaymentView(View):
    def get(self, *args, **kwargs):
        # order = Order.objects.get(user=self.request.user, ordered=False)
        bill = Address.objects.get(email=self.request.session['email'])
        if bill:
            context = {
                # 'order': order,
                # 'DISPLAY_COUPON_FORM': False,
                'STRIPE_PUBLIC_KEY' : settings.STRIPE_PUBLIC_KEY
            }
            # userprofile = self.request.user.userprofile
            # if userprofile.one_click_purchasing:
            #     # fetch the users card list
            #     cards = stripe.Customer.list_sources(
            #         userprofile.stripe_customer_id,
            #         limit=3,
            #         object='card'
            #     )
            #     card_list = cards['data']
            #     if len(card_list) > 0:
            #         # update the context with the default card
            #         context.update({
            #             'card': card_list[0]
            #         })
            return render(self.request, "payment.html", context)
        else:
            messages.warning(
                self.request, "You have not added a billing address")
            return redirect("checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)
        userprofile = UserProfile.objects.get(user=self.request.user)
        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')

            if save:
                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(
                        userprofile.stripe_customer_id)
                    customer.sources.create(source=token)

                else:
                    customer = stripe.Customer.create(
                        email=self.request.user.email,
                    )
                    customer.sources.create(source=token)
                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()

            amount = int(order.get_total() * 100)

            try:

                if use_default or save:
                    # charge the customer because we cannot charge the token more than once
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        customer=userprofile.stripe_customer_id
                    )
                else:
                    # charge once off on the token
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        source=token
                    )

                # create the payment
                payment = Payment()
                payment.stripe_charge_id = charge['id']
                payment.user = self.request.user
                payment.amount = order.get_total()
                payment.save()

                # assign the payment to the order

                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                order.ordered = True
                order.payment = payment
                order.ref_code = create_ref_code()
                order.save()

                messages.success(self.request, "Your Payment is Successful")
                return redirect("/")

            except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                messages.warning(self.request, f"{err.get('message')}")
                return redirect("/")

            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.warning(self.request, "Rate limit error")
                return redirect("/")

            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                print(e)
                messages.warning(self.request, "Invalid parameters")
                return redirect("/")

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                messages.warning(self.request, "Not authenticated")
                return redirect("/")

            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.warning(self.request, "Network error")
                return redirect("/")

            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                messages.warning(
                    self.request, "Something went wrong. You were not charged. Please try again.")
                return redirect("/")

            except Exception as e:
                # send an email to ourselves
                messages.warning(
                    self.request, "A serious error occurred. We have been notifed.")
                return redirect("/")

        messages.warning(self.request, "Invalid data received")
        return redirect("/payment/stripe/")

def match_caregiver_to_senior(request, caregiver_id) :
    # return HttpResponse("<h1> Hey" + str(caregiver_id) + "</h1>")
    context = {}
    if 'email' in request.session :
        senior_email = request.session['email']
    caregiver_obj = Caregiver.objects.get(id=caregiver_id)
    context['caregiver'] = caregiver_obj
    if request.method == 'POST' :
        record = Match.objects.create(
            senior_email=senior_email,
            caregiver_email=caregiver_obj.email)
    #return redirect('match_caregiver_to_senior/')
    return render(request, 'caregiver_details_for_senior.html', context)

def display_matched_caregivers(request, *args, **kwargs) :
    context = {}
    if 'email' in request.session :
        #The user is already logged in
        email = request.session['email']
        record = Match.objects.get(senior_email = email)
        context['caregiver'] = Caregiver.objects.get(email = record.caregiver_email)
        return render(request, 'display_matched_caregivers.html', context)

