from django.shortcuts import render
from django.http import HttpResponse
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import RegistrationDetails
from django.core.mail import send_mail
from django.contrib.staticfiles.templatetags.staticfiles import static
# Create your views here.


def campus_ambassador_home(request):
    return render(request, 'campus_ambassador/index.html')


# def campus_ambassador_register(request):
# 	return render(request, 'campus_ambassador/registrations_closed.html')


@login_required
def campus_ambassador_register(request):

    try:
        prev_registration_details = RegistrationDetails.objects.get(user=request.user)
    except RegistrationDetails.DoesNotExist:
        prev_registration_details = None

    # if form has already been submitted
    if prev_registration_details:
        return render(request, 'campus_ambassador/already_registered.html')

    # have a look at Social accounts Field in django admin
    # you will get it
    request.user.email = SocialAccount.objects.get(user=request.user).extra_data.get("email")
    request.user.save()

    if request.method == "POST":
        # edit: this is not saving the user itself
        # but on my windows environment, it wasn't raising integrity error
        campus_ambassador_registration_details_form = CampusAmbassadorRegistrationDetailsForm(request.POST)
        if campus_ambassador_registration_details_form.is_valid():
            new_campus_ambassador_registration = campus_ambassador_registration_details_form.save(commit=False)
            new_campus_ambassador_registration.user = request.user
            new_campus_ambassador_registration.campus_ambassador_code = (str(request.user.first_name)[:4]).upper() + str(request.user.id) + 'Z19'
            new_campus_ambassador_registration.save()
            # send_mail(
            #     'Successful Registration for Campus Ambassador program for Zeitgeist 2k21',
            #     'Dear ' + str(request.user.first_name) + ' ' + str(request.user.last_name) + '\n\nYou are successfully registered for Campus Ambassador program for Zeitgeist 2k21. We are excited for your journey with us.\n\nYour CAMPUS AMBASSADOR CODE is ' + str(new_campus_ambassador_registration.campus_ambassador_code) + '. Please read the Campus Ambassador Policy here - https://' + request.get_host() + static('campus_ambassador/CA.pdf') + '.\n\nWe wish you best of luck. Give your best and earn exciting prizes !!!\n\nRegards\nZeitgeist 2k21 Public Relations Team',
            #     'zeitgeist.pr@iitrpr.ac.in',
            #     [request.user.email],
            #     fail_silently=False,
            # )
            return render(request, 'campus_ambassador/success.html')
    else:
        campus_ambassador_registration_details_form = CampusAmbassadorRegistrationDetailsForm()

    return render(request, 'campus_ambassador/register.html',
        {'campus_ambassador_registration_details_form': campus_ambassador_registration_details_form})
