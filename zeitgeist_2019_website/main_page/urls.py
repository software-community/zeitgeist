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
from django.views.generic.base import RedirectView, TemplateView
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewsSitemap

router = routers.DefaultRouter()
router.register(r'cats', api.CategoryViewSet)
router.register(r'subcats', api.SubcategoryViewSet)
router.register(r'events', api.EventViewSet)
router.register(r'our_sponsor', api.Our_SponsorViewSet)
router.register(r'prev_sponsor', api.Prev_SponsorViewSet)
router.register(r'notification', api.NotificationViewSet)

sitemaps = {'static':StaticViewsSitemap}

urlpatterns = [
    path('', views.main_page_home, name="main_page_home"),
    path('workshop/', RedirectView.as_view(pattern_name="workshop_tech", permanent=True)),
    path('workshop/tech/', views.workshop,  {'type':'tech'}, name="workshop_tech"),
    path('workshop/cult/', views.workshop, {'type':'cult'}, name="workshop_cult"),
    path('register_as_participant/', views.register_as_participant,
         name="register_as_participant"),
    path('tech_events/', views.tech_events, name="tech_events"),
    path('club_details/<int:club_id>/', views.club_details, name='club_details'),
    path('club_details/<int:event_id>/coupon/', views.cashless_reg_page, name='cashless_reg_page'),
    path('merchandise/', views.merchandise, name="merchandise"),
    path('cult_events/', views.cult_events, name="cult_events"),
    path('terms_and_conditions/', views.tnc, name="tnc"),
    path('profile/', views.profile, name="profile"),
    path('schedule/', views.schedule, name="schedule"),
    path('temp/', views.schedule2, name="schedule2"),
    path('verify_user/', views.verify_user, name="verify_user"),
    path('admin_control/', views.admin_control, name='admin_control'),
    path('feedback_form/', views.feedback_form, name='feedback_form'),
    path('register/<int:event_id>/',
        views.register_for_event, name="register_for_event"),
    path('data-api/', include(router.urls)),
    path('reach_us/', views.reach_us, name='reach_us'),

    path('pay/<int:event_id>/', views.pay_for_event, name="pay_for_event"),
    path('webhook/', csrf_exempt(views.weebhook), name="webhook"),
    path('payment_redirect/', views.payment_redirect, name="payment_redirect"),

    path('support/', views.support, name="support"),
    path('support_weebhook/', csrf_exempt(views.support_weebhook),
         name="support_weebhook"),
    path('support_payment_redirect/', views.support_payment_redirect,
         name="support_payment_redirect"),



    path('send-mail/', views.send_email_all, name='send_email_all'),

    # define the login URLs
    # since i haven't used allauth.urls, hence many pages like account/login etc won't be accessible
    path('accounts/', include('allauth.socialaccount.providers.google.urls')),

    # just to define account_email, account_login, account_signup, socialaccount_login, socialaccount_signup
    # to resolve internal server error issue
    path('accounts/google/login/', RedirectView.as_view(pattern_name='google_login',
                                                        permanent=True), name="account_login"),
    path('accounts/google/login/', RedirectView.as_view(pattern_name='google_login',
                                                        permanent=True), name="account_signup"),
    path('accounts/google/login/', RedirectView.as_view(pattern_name='google_login',
                                                        permanent=True), name="socialaccount_login"),
    path('accounts/google/login/', RedirectView.as_view(pattern_name='google_login',
                                                        permanent=True), name="socialaccount_signup"),

    # define the logout URL
    path('accounts/google/logout/',
         auth_views.LogoutView.as_view(), name="google_logout"),

    # just to define account_logout
    # to resolve internal server error issue
    path('accounts/google/logout/',
         auth_views.LogoutView.as_view(), name="account_logout"),

    # for account change, which logs the user out and then redirects to account_login
    path('accounts/change_account/', views.change_account, name="account_email"),

    # if somehow django redirects to accounts/logout
    # due to internal failures
    path('accounts/logout/', RedirectView.as_view(pattern_name='google_logout',
                                                  permanent=True), name="go_to_google_logout"),

    # if somehow django redirects to accounts/login
    # due to internal failures
    # it might occur when accounts/google/login fails and hence redirects to accounts/login
    path('accounts/login/', RedirectView.as_view(pattern_name='google_login',
                                                 permanent=False), name="go_to_google_login"),

    path('robots.txt', TemplateView.as_view(template_name="main_page/robots.txt", content_type='text/plain')),
    path('sitemap.xml', sitemap, {'sitemaps':sitemaps}),
]
