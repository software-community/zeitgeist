from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.urls import reverse
from urllib.parse import urlparse
# Create your views here.

def home(request):
    return render(request, 'main_page/index.html')

# if some other page redirects us to change_account, then 404 will happen
# but why will some other page redirect to here
def change_account(request):
    prev_page = request.META.get('HTTP_REFERER', reverse('main_page_home'))
    _next = urlparse(prev_page).path
    logout(request)
    return redirect(reverse('google_login')+'?next='+_next)
