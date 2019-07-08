from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'campus_ambassador/index.html')

def register(request):
    return HttpResponse("Make the registration page")
