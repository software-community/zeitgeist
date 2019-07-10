from django.shortcuts import render, redirect, HttpResponseRedirect
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
    else:
        return HttpResponseRedirect('/accounts/login/')


def submit_detail(request):
    print(request)
    #save data
