"""zeitgeist_2019_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from . import views
from . import api
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'cats', api.CategoryViewSet)
router.register(r'subcats', api.SubcategoryViewSet)
router.register(r'events', api.EventViewSet)
router.register(r'our_sponsor', api.Our_SponsorViewSet)
# router.register(r'prev_sponsor', api.Prev_SponsorViewSet)

urlpatterns = [
    path('', views.main_page_home, name="main_page_home"),
    path('register_as_participant/', views.register_as_participant, name="register_as_participant"),
    path('events/', views.main_page_events, name="main_page_events"),
    path('register/<int:event_id>/', views.register_for_event, name="register_for_event"),
    path('pay/<int:subcategory_id>/', views.pay_for_subcategory, name="pay_for_subcategory"),
    path('webhook/', csrf_exempt(views.weebhook), name="webhook"),
    path('payment_redirect/', views.payment_redirect, name="payment_redirect"),
    path('support/', views.support, name="support"),
    path('swiggy_launchpad', views.swiggy_launchpad, name='swiggy_launchpad'),
    path('data-api/', include(router.urls)),

    path('accomodation_weebhook/', csrf_exempt(views.accomodation_weebhook), name='accomodation_weebhook'),
    path('accomodation_payment_redirect/', views.accomodation_payment_redirect, name='accomodation_payment_redirect'),
    path('accomodation/', views.accomodation, name='accomodation'),
    path('accomodation_for/<int:number_of_people_to_accomodate>/', views.accomodation, name='accomodation_for'),

    # define the login URLs
    # since i haven't used allauth.urls, hence many pages like account/login etc won't be accessible
    path('accounts/', include('allauth.socialaccount.providers.google.urls')),

    # just to define account_email, account_login, account_signup, socialaccount_login, socialaccount_signup
    # to resolve internal server error issue
    path('accounts/google/login/', RedirectView.as_view(pattern_name='google_login', permanent=True), name="account_login"),
    path('accounts/google/login/', RedirectView.as_view(pattern_name='google_login', permanent=True), name="account_signup"),
    path('accounts/google/login/', RedirectView.as_view(pattern_name='google_login', permanent=True), name="socialaccount_login"),
    path('accounts/google/login/', RedirectView.as_view(pattern_name='google_login', permanent=True), name="socialaccount_signup"),

    # define the logout URL
    path('accounts/google/logout/', auth_views.LogoutView.as_view(), name = "google_logout"),

    # just to define account_logout
    # to resolve internal server error issue
    path('accounts/google/logout/', auth_views.LogoutView.as_view(), name = "account_logout"),

    # for account change, which logs the user out and then redirects to account_login
    path('accounts/change_account/', views.change_account, name="account_email"),

    # if somehow django redirects to accounts/logout
    # due to internal failures
    path('accounts/logout/', RedirectView.as_view(pattern_name='google_logout', permanent=True), name="go_to_google_logout"),

    # if somehow django redirects to accounts/login
    # due to internal failures
    # it might occur when accounts/google/login fails and hence redirects to accounts/login
    path('accounts/login/', RedirectView.as_view(pattern_name='google_login', permanent=False), name="go_to_google_login"),
]
