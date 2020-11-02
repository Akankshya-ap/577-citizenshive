from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from .models import CommonRegistration, Senior, Caregiver, Posts, Comments
import json
# from pyzipcode import ZipCodeDatabase  

# Create your views here.

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
    return render(request, 'caregiver_details_for_senior.html', context)

def view_senior_details(request, senior_id) :
    context = {}
    senior_obj = Senior.objects.get(id=senior_id)
    context['caregiver'] = senior_obj
    return render(request, 'senior_details_for_caregiver.html', context)

def search_caregivers(request, *args, **kwargs) :
    context = {}
    # zcdb = ZipCodeDatabase()
    # in_radius = [z.zip for z in zcdb.get_zipcodes_around_radius('90007', 8)] # ('ZIP', radius in miles)
    # radius_utf = [x.encode('UTF-8') for x in in_radius] # unicode list to utf list
    # context['data'] = radius_utf
    # zip, gender, radius
    if request.method == 'POST' :
        zip_code = request.POST['zip']
        radius = int(request.POST['radius'])
        # zcdb = ZipCodeDatabase() 
        # in_radius = [z.zip for z in zcdb.get_zipcodes_around_radius(zip_code, radius)] # ('ZIP', radius in miles)
        # radius_utf = [x.encode('UTF-8') for x in in_radius] # unicode list to utf list
        # radius_arr = [x.encode('utf-8').decode('unicode-escape') for x in in_radius]
        radius_arr = 10 #added 28/10
        caregivers = Caregiver.objects.filter(zip_code__in = radius_arr)
        context['caregivers'] = caregivers
        context['isPostRequest'] = True
    else :
        context['caregivers'] = []
        context['isPostRequest'] = False
    return render(request, 'search_caregivers.html', context)

def search_seniors(request, *args, **kwargs) :
    context = {}
    # zcdb = ZipCodeDatabase()
    # in_radius = [z.zip for z in zcdb.get_zipcodes_around_radius('90007', 8)] # ('ZIP', radius in miles)
    # radius_utf = [x.encode('UTF-8') for x in in_radius] # unicode list to utf list
    # context['data'] = radius_utf
    # zip, gender, radius
    if request.method == 'POST' :
        zip_code = request.POST['zip']
        radius = int(request.POST['radius'])
        # zcdb = ZipCodeDatabase() 
        # in_radius = [z.zip for z in zcdb.get_zipcodes_around_radius(zip_code, radius)] # ('ZIP', radius in miles)
        # radius_utf = [x.encode('UTF-8') for x in in_radius] # unicode list to utf list
        # radius_arr = [x.encode('utf-8').decode('unicode-escape') for x in in_radius]
        radius_arr = 10 #added 28/10
        seniors = Senior.objects.filter(zip_code__in = radius_arr)
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
    if request.method == 'POST' :
        name = request.POST['name']
        email = request.POST['email']
        dob = request.POST['dob']
        availability = request.POST['availability']
        zip_code = request.POST['zip']
        city = request.POST['city']
        state = request.POST['state']
        bio = request.POST['bio']

        record = Caregiver.objects.get(email=email)
        record.name = name
        record.availability = availability
        record.zip_code = zip_code
        record.city = city
        record.state = state
        record.bio = bio
        record.dob = dob if dob!="" else None
        record.save()
        context['record'] = record
    else :
        context['record'] = Caregiver.objects.get(email = request.session['email'])
    return render(request, 'caregiver_dashboard.html', context)


def senior_dashboard_view(request, *args, **kwargs) :
    context = {}
    if request.method == 'POST' :
        name = request.POST['name']
        email = request.POST['email']
        dob = request.POST['dob']
        availability = request.POST['availability']
        zip_code = request.POST['zip']
        city = request.POST['city']
        state = request.POST['state']
        bio = request.POST['bio']
        profile_image = request.FILES['profile_image']

        record = Senior.objects.get(email=email)
        record.name = name
        record.availability = availability
        record.zip_code = zip_code
        record.city = city
        record.state = state
        record.bio = bio
        record.dob = dob if dob!="" else None
        record.profile_image = profile_image

        record.save()
        context['record'] = record
        # context['profile_image_url'] = record.profile_image.url
        # context['image_object'] = record.profile_image
    else :
        context['record'] = Senior.objects.get(email = request.session['email'])
        # context['profile_image_url'] = 'default'
        # context['image_object'] = record.profile_image
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

        #Add values to the session
        # request.session['isLoggedIn']  = True
        # request.session['email'] = email
        # request.session['userType'] = user_type

        if user_type == 'senior' :
            return render(request, 'senior_dashboard.html', context)
        else :
            return render(request, 'caregiver_dashboard.html', context)
        


def landing_page(request, *args, **kwargs) :
    # return HttpResponse("<h1> Hello Mugdha </h1>")
    context = {}
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
    return render(request, 'about_us.html', context)

