from django.contrib import admin
from django.urls import path,include
from django.views.decorators.csrf import csrf_exempt
from . import views
from django.contrib.auth import views as auth_views
app_name='TSP'

urlpatterns=[
    path('', views.home,name='home'),
    path('profile/', views.profile,name='profile'),
    path('profile/edit/', views.register_profile,name='register_profile'),
    path('accounts/google/logout/', auth_views.LogoutView.as_view(), name = "account_logout"),
    path('payment-form/', views.fee_payment,name='payment_view'),
    path('payment_redirect/', views.payment_redirect, name = 'payment_redirect'),
    path('webhook/', csrf_exempt(views.webhook), name= 'payment_webhook'),

    path('result/', views.result_view,name='result'),
    path('load-data/', views.upload_tsp_data,name='load_data'),
    path('test/', views.test),
]
