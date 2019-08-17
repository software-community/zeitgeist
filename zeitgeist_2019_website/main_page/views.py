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

def event_view(request, event_id):
    event = Event.objects.get(id = event_id)
    return render(request, 'main_page/event_view.html', {'event' : event})

@login_required
def register_as_participant(request):

    try:
        prev_registration_details = Participant.objects.get(user=request.user)
    except Participant.DoesNotExist:
        prev_registration_details = None

    # if user is already registered as a participant
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
            new_registration.participant_code = (str(request.user.first_name)[:4]).upper() + str(request.user.id) + 'Z19'
            new_registration.save()
            send_mail(
                'Welcome to Zeitgeist 2k19',
                'Dear ' + str(request.user.first_name) + ' ' + str(request.user.last_name) + '\n\nThank you for showing your interest in Zeitgeist 2k19. We are excited for your journey with us and wish you luck for all the events that you take part in.\n\nYour PARTICIPANT CODE is ' + str(new_registration.participant_code) + '. If you are also a Campus Ambassador for Zeitgeist 2k19, your PARTICIPANT CODE is also the same as your CAMPUS AMBASSADOR code.\n\nWe wish you best of luck. Give your best and earn exciting prizes !!!\n\nRegards\nZeitgeist 2k19 Public Relations Team',
                'zeitgeist.pr@iitrpr.ac.in',
                [request.user.email],
                fail_silently=False,
            )
            return render(request, 'main_page/success.html')
    else:
        participant_registration_details_form = ParticipantRegistrationDetailsForm()

    return render(request, 'main_page/register.html',
        {'participant_registration_details_form': participant_registration_details_form})

def register_for_event(request):

    try:
        prev_registration_details = Participant.objects.get(user=request.user)
    except Participant.DoesNotExist:
        prev_registration_details = None

    # if user has not yet registered as a participant
    if prev_registration_details == None:
        return register_as_participant(request)

    # No need to create form for solo events
    # If event_type is duet or group, then create a form and get the details
    # Note that same form can be used in duet or group events (duet also has team name)
    # Just check the event_type, minimum_team_size, maximum_team_size
    # and render the form accordingly
    # We collect name, email and mobile number of each team member who has not already a participant
    # and first create their user model, then create their participant model (and create
    # participant_code for each participant the same way as done in register_as_participant)
    # Then we do 7 things:
    # 1. We send email to each individual newly made (who was not a participant earlier)
    # participant separately about their participant_code
    # 2. After successful payment, we add each participant to ParticipantHasPaid table
    # 3. We add each participant to ParticipantHasParticipated table
    # 4. We add each participant to TeamHasMember table
    # 5. We create a unique Team Code just like we created unique CA Code (Divyanshu will help)
    # 6. We send email to the whole team about their participation (Divyanshu will take care of the content of the email)
    # 7. Show success page
    # Note: Remember to use TeamRegistrationDetailsForm as a part of the form
    # Note: Give option of registering team member by entering his participant_code so that
    # participants who have already paid for the subcategory do not pay again
    # then we don't need to ask for that user's mobile number and email since he is already registered
    # Also, payment should be calculated by seeing that
    # how many participants of the team have already paid for this even't subcategory
    # Note: Some people might still type email and mobile for participants who have already registered
    # so we need to check each email address and get the associated user and check if he has already paid or not

    # For solo events, just redirect to payment portal, then do 5 things:
    # 1. If user has not already paid for that subcategory, then
    # after successful payment, add the participant to ParticipantHasPaid table
    # 2. Add the participant to ParticipantHasParticipated table
    # 3. Add the participant to TeamHasMember table
    # 5. We send email to the participant about their participation (Divyanshu will take care of the content of the email)
    # 6. Show success page
