from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.urls import reverse
from urllib.parse import urlparse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from django.core.mail import send_mail
from django.contrib.staticfiles.templatetags.staticfiles import static
# Create your views here.

def main_page_home(request):
    return render(request, 'main_page/index.html')

# if some other page redirects us to change_account, then 404 will happen
# but why will some other page redirect to here
def change_account(request):
    prev_page = request.META.get('HTTP_REFERER', reverse('main_page_home'))
    _next = urlparse(prev_page).path
    logout(request)
    return redirect(reverse('google_login')+'?next='+_next)

def main_page_events(request):

    events_data = {}
    categories = Category.objects.all()
    for category in categories:
        events_data[category] = {}
        subcategories = category.subcategory_set.all()
        for subcategory in subcategories:
            events_data[category][subcategory] = subcategory.event_set.all()

    print(events_data)

    return render(request, 'main_page/events.html', {'events_data' : events_data})

@login_required
def register_as_participant(request):

    try:
        prev_registration_details = Participant.objects.get(user=request.user)
    except Participant.DoesNotExist:
        prev_registration_details = None

    # if form has already been submitted
    if prev_registration_details:
        return render(request, 'main_page/already_registered.html')

    # have a look at Social accounts Field in django admin
    # you will get it
    request.user.email = SocialAccount.objects.get(user=request.user).extra_data.get("email")
    request.user.save()

    if request.method == "POST":
        # edit: this is not saving the user itself
        # but on my windows environment, it wasn't raising integrity error
        participant_registration_details_form = ParticipantRegistrationDetailsForm(request.POST)
        if participant_registration_details_form.is_valid():
            new_registration = participant_registration_details_form.save(commit=False)
            new_registration.user = request.user
            new_registration.main_page_code = (str(request.user.first_name)[:4]).upper() + str(request.user.id) + 'Z19'
            new_registration.save()
            send_mail(
                'Successful Registration for Campus Ambassador program for Zeitgeist 2k19',
                'Dear ' + str(request.user.first_name) + ' ' + str(request.user.last_name) + '\n\nYou are successfully registered for Campus Ambassador program for Zeitgeist 2k19. We are excited for your journey with us.\n\nYour CAMPUS AMBASSADOR CODE is ' + str(new_registration.main_page_code) + '. Please read the Campus Ambassador Policy here - https://' + request.get_host() + static('main_page/CA.pdf') + '.\n\nWe wish you best of luck. Give your best and earn exciting prizes !!!\n\nRegards\nZeitgeist 2k19 Public Relations Team',
                'zeitgeist.pr@iitrpr.ac.in',
                [request.user.email],
                fail_silently=False,
            )
            return render(request, 'main_page/success.html')
    else:
        participant_registration_details_form = ParticipantRegistrationDetailsForm()

    return render(request, 'main_page/register.html',
        {'participant_registration_details_form': participant_registration_details_form})
