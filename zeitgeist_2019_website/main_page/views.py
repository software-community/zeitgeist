from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout
# Create your views here.

def home(request):
    return render(request, 'main_page/index.html')

def change_email(request):
    logout(request)
    return redirect('account_login')
