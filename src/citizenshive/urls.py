"""citizenshive URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from app1.views import landing_page, registration_page, handle_login, forum, add_new_post, add_post_comment, senior_dashboard_view, caregiver_dashboard_view, search_caregivers, view_caregiver_details, logout, dashboard_view, about_us, search_seniors, view_senior_details, room_detail, all_rooms, token, add_or_get_chatroom, get_chats, payment_summary, CheckoutView, services, contact, PaymentView, display_matched_caregivers,display_matched_seniors, match_caregiver_to_senior, rating_review, pay_order, visit_profile
from pyzipcode import ZipCodeDatabase


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name = 'landing_page'),
    path('registration', registration_page, name = 'registration_page'),
    path('handle_login', handle_login, name='handle_login'),
    path('forum', forum, name='forum'),
    path('add_new_post', add_new_post, name='add_new_post' ),
    path('add_post_comment', add_post_comment, name='add_post_comment'),
    path('senior_dashboard_view', senior_dashboard_view, name='senior_dashboard_view'),
    path('caregiver_dashboard_view', caregiver_dashboard_view, name='caregiver_dashboard_view'),
    path('search_caregivers', search_caregivers, name='search_caregivers'),
    path('view_caregiver_details/<int:caregiver_id>', view_caregiver_details, name='view_caregiver_details'),
    path('search_seniors', search_seniors, name='search_seniors'),
    path('view_senior_details/<int:senior_id>', view_senior_details, name='view_senior_details'),
    path('logout', logout, name='logout'),
    path('dashboard_view', dashboard_view, name='dashboard_view'),
    path('about_us', about_us, name='about_us'),
    path('all_rooms/', all_rooms, name = 'all_rooms'),
    url(r'rooms/(?P<slug>[-\w]+)/$', room_detail, name="room_detail"),
    url(r'token$',token, name="token" ),
    path('add_or_get_chatroom/<int:user_id>', add_or_get_chatroom, name='add_or_get_chatroom'),
    path('get_chats', get_chats, name='get_chats'),
    path('payment_summary',payment_summary, name='payment_summary'),
    path('checkout',CheckoutView.as_view(), name='checkout'),
    path('services', services, name='services'),
    path('contact', contact, name='contact'),
    path('payment',PaymentView.as_view(),name='payment'),
    path('display_matched_caregivers', display_matched_caregivers, name='display_matched_caregivers'),
    path('match_caregiver_to_senior/<int:caregiver_id>', match_caregiver_to_senior, name='match_caregiver_to_senior'),
    path('rating_review', rating_review, name='rating_review'),
    path('pay_order/<str:caregiver_email>', pay_order, name='pay_order'),
    path('display_matched_seniors', display_matched_seniors, name='display_matched_seniors'),
    path('visit_profile/<int:caregiver_id>', visit_profile, name='visit_profile')

]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
