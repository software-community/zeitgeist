from django.shortcuts import render, redirect
from django.http import HttpResponse
from allauth.socialaccount.models import SocialAccount

# Create your views here.

def home(request):
    return render(request, 'campus_ambassador/index.html')

def register(request):
    # have a look at Social accounts Field in django admin
    # you will get it
    if request.user.is_authenticated:
        request.user.email = SocialAccount.objects.get(user=request.user).extra_data.get("email")
        request.user.save()
    return render(request, 'campus_ambassador/register.html')
