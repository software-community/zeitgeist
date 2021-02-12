import hashlib
import hmac
import os
import datetime
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
from django.http import HttpResponseServerError
from .methods import *
from django.forms import formset_factory, modelformset_factory
from django.http import HttpResponseNotFound
import csv
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.


def main_page_home(request):
    our_sponsors = Our_Sponsor.objects.all().order_by('id')
    prev_sponsors = Prev_Sponsor.objects.all()
    events_11_oct = Event.objects.filter(start_date_time__startswith='2019-10-11').order_by('start_date_time')
    events_12_oct = Event.objects.filter(start_date_time__startswith='2019-10-12').order_by('start_date_time')
    events_13_oct = Event.objects.filter(start_date_time__startswith='2019-10-13').order_by('start_date_time')
    context = {'our_sponsors': our_sponsors, 'prev_sponsors': prev_sponsors, 'events_11_oct': events_11_oct, 'events_12_oct': events_12_oct, 'events_13_oct': events_13_oct}
    return render(request, 'main_page/index.html', context)


def change_account(request):
    '''
    If some other page redirects us to change_account, then 404 will happen
    but why will some other page redirect to here
    '''
    prev_page = request.META.get('HTTP_REFERER', reverse('main_page_home'))
    _next = urlparse(prev_page).path
    logout(request)
    return redirect(reverse('google_login')+'?next='+_next)


@login_required
def register_as_participant(request):

    try:
        prev_participant_registration_details = Participant.objects.get(
            participating_user=request.user)
    except Participant.DoesNotExist:
        prev_participant_registration_details = None

    if prev_participant_registration_details:
        return render(request, 'main_page/already_registered_as_participant.html')

    request.user.email = SocialAccount.objects.get(
        user=request.user).extra_data.get("email")
    request.user.save()

    if request.method == "POST":
        participant_registration_details_form = ParticipantRegistrationDetailsForm(
            request.POST)
        if participant_registration_details_form.is_valid():
            new_participant_registration = participant_registration_details_form.save(
                commit=False)
            new_participant_registration.participating_user = request.user
            new_participant_registration.participant_code = (str(request.user.first_name)[
                :4]).upper() + str(request.user.id) + 'Z19'
            new_participant_registration.save()
            # send_mail(
            #     'Welcome to Zeitgeist 2k21',
            #     'Dear ' + str(new_participant_registration.name) + '\n\nThank you for showing your interest in Zeitgeist 2k21. We are excited for your journey with us and wish you luck for all the events that you take part in.\n\nYour PARTICIPANT CODE is ' + str(
            #         new_participant_registration.participant_code) + '. If you are also a Campus Ambassador for Zeitgeist 2k21, your PARTICIPANT CODE is also the same as your CAMPUS AMBASSADOR CODE.\n\nNote that this email is not for your participation in any event. To participate in events, you need to register for them on the Events page of Zeitgeist website. We wish you best of luck. Give your best and stand a chance to win exciting prizes !!!\n\nRegards\nZeitgeist 2k21 Public Relations Team',
            #     'zeitgeist.pr@iitrpr.ac.in',
            #     [new_participant_registration.participating_user.email],
            #     fail_silently=False,
            # )
            return render(request, 'main_page/register_as_participant_success.html')
    else:
        participant_registration_details_form = ParticipantRegistrationDetailsForm()

    return render(request, 'main_page/register_as_participant.html',
                  {'participant_registration_details_form': participant_registration_details_form})


def main_page_events(request):

    events_data = {}
    categories = Category.objects.all()
    for category in categories:
        events_data[category] = {}
        subcategories = category.subcategory_set.all()
        for subcategory in subcategories:
            events_data[category][subcategory] = subcategory.event_set.all()
    return render(request, 'main_page/events.html', {'events_data': events_data})


@login_required
def register_for_event(request, event_id):

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return HttpResponseNotFound()

    if event.subcategory.participation_fees_per_person == 0:
        return HttpResponseNotFound()

    try:
        participant = Participant.objects.get(participating_user=request.user)
    except Participant.DoesNotExist:
        return render(request, 'main_page/must_register_as_participant_first.html')

    try:
        ParticipantHasParticipated.objects.get(
            participant=participant, event=event)
        # code did not blow, hence participant has already participated in this event
        return render(request, 'main_page/already_registered_in_event.html')
    except:
        pass

    if event.event_type == 'Solo':
        try:
            payment_details = ParticipantHasPaid.objects.get(
                participant=participant, paid_subcategory=event.subcategory)
            if payment_details.transaction_id == '-1' or payment_details.transaction_id == '0':
                context = {'event': event, 'events_in_subcategory': Event.objects.filter(
                    subcategory=event.subcategory)}
                return render(request, 'main_page/must_pay_for_subcategory_first.html', context)
        except ParticipantHasPaid.DoesNotExist:
            context = {'event': event, 'events_in_subcategory': Event.objects.filter(
                subcategory=event.subcategory)}
            return render(request, 'main_page/must_pay_for_subcategory_first.html', context)
        ParticipantHasParticipated.objects.create(
            participant=participant, event=event)
        # send_mail(
        #     'Participation in ' + str(event.name) + ' in Zeitgeist 2k21',
        #     'Dear ' + str(participant.name) + '\n\nThank you for participating in ' + str(event.name) + '. Please carry a Photo ID Proof with you for your onsite registration, otherwise your registration might get cancelled. We wish you best of luck. Give your best and stand a chance to win exciting prizes !!!\n\nReminder - Your PARTICIPANT CODE is ' + str(
        #         participant.participant_code) + '. If you are also a Campus Ambassador for Zeitgeist 2k21, your PARTICIPANT CODE is also the same as your CAMPUS AMBASSADOR CODE.\n\nRegards\nZeitgeist 2k21 Public Relations Team',
        #     'zeitgeist.pr@iitrpr.ac.in',
        #     [participant.participating_user.email],
        #     fail_silently=False,
        # )
        context = {'event': event}
        return render(request, 'main_page/register_in_solo_event_success.html', context)

    else:
        TeamHasMemberFormSet = formset_factory(form=TeamHasMemberForm, formset=BaseTeamFormSet, extra=event.maximum_team_size-1,
                                               max_num=event.maximum_team_size, validate_max=True, min_num=event.minimum_team_size, validate_min=True)
        if request.method == "POST":
            list_of_team_members = []
            list_of_email_addresses_of_team_members = []
            team_member_formset = TeamHasMemberFormSet(request.POST, initial=[
                                                       {'team_member': str(participant.participant_code)}], prefix='team_member')
            team_form = TeamForm(request.POST)
            if team_member_formset.is_valid() and team_form.is_valid():
                for team_member_form in team_member_formset:
                    team_member = team_member_form.cleaned_data.get(
                        'team_member')
                    # if form was empty
                    if not team_member:
                        continue
                    list_of_team_members.append(team_member)
                    list_of_email_addresses_of_team_members.append(
                        team_member.participating_user.email)
                    # since participant is already validated, his model must exist
                    try:
                        team_member_payment = ParticipantHasPaid.objects.get(
                            participant=team_member, paid_subcategory=event.subcategory)
                        if team_member_payment.transaction_id == '-1' or team_member_payment.transaction_id == '0':
                            return render(request, 'main_page/some_team_members_have_not_paid.html', {'member_who_has_not_paid': team_member})
                    except ParticipantHasPaid.DoesNotExist:
                        return render(request, 'main_page/some_team_members_have_not_paid.html', {'member_who_has_not_paid': team_member})
                # print(team_form.cleaned_data)
                new_team = team_form.save(commit=False)
                temp_team_code = str(
                    request.user.id) + datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
                new_team.team_code = temp_team_code
                new_team.event = event
                new_team.captain = participant
                new_team.save()
                new_team = Team.objects.get(team_code=temp_team_code)
                new_team_code = ((str(new_team.name).replace(" ", ""))[
                                 :4]).upper() + str(new_team.id) + 'Z19'
                new_team.team_code = new_team_code
                new_team.save()
                new_team = Team.objects.get(team_code=new_team_code)
                for team_member in list_of_team_members:
                    ParticipantHasParticipated.objects.create(
                        participant=team_member, event=event)
                    TeamHasMember.objects.create(
                        team=new_team, member=team_member)
                # send_mail(
                #     'Participation in ' +
                #     str(event.name) + ' in Zeitgeist 2k21',
                #     'Dear ' + str(new_team.name) + '\n\nThank you for participating in ' + str(event.name) + '. Each of you must carry a Photo ID Proof with you for your onsite registration, otherwise your registration might get cancelled.\n\nYour TEAM CODE is ' + str(
                #         new_team.team_code) + '. We wish you best of luck. Give your best and stand a chance to win exciting prizes !!!\n\nRegards\nZeitgeist 2k21 Public Relations Team',
                #     'zeitgeist.pr@iitrpr.ac.in',
                #     list_of_email_addresses_of_team_members,
                #     fail_silently=False,
                # )
                context = {'event': event, 'team': new_team}
                return render(request, 'main_page/register_in_group_event_success.html')
        else:
            team_form = TeamForm()
            team_member_formset = TeamHasMemberFormSet(
                initial=[{'team_member': str(participant.participant_code)}], prefix='team_member')

        return render(request, 'main_page/register_team.html',
                      {'event': event,
                       'team_form': team_form,
                       'team_member_formset': team_member_formset,
                       })


@login_required
def pay_for_event(request, event_id):

    # if subcategory_id != 19:
    #     return render(request, 'main_page/registrations_closed.html')

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        # if no such Event exists
        return HttpResponseNotFound()

    if event.participation_fees_per_person == 0:
        return HttpResponseNotFound()

    try:
        participant = Participant.objects.get(participating_user=request.user)
    except Participant.DoesNotExist:
        return render(request, 'main_page/must_register_as_participant_first.html')

    participanthaspaid = None

    try:
        participanthaspaid = ParticipantHasPaid.objects.get(
            participant=participant, paid_event=event)
        if participanthaspaid.transaction_id == '0' or participanthaspaid.transaction_id == '-1':
            raise Exception("Previous payment was a failure !")
        return render(request, 'main_page/already_registered_in_event.html')
    except:
        pass

    purpose = str(event.name).upper() + ' OF ' + str(event.subcategory.category.name).upper()
    response = payment_request(participant.name, event.participation_fees_per_person, purpose,
                               request.user.email, participant.contact_mobile_number.__str__())
    print(response)
    if response['success']:
        url = response['payment_request']['longurl']
        payment_request_id = response['payment_request']['id']
        # if previous payment was unsuccessful, update payment_request_id
        if participanthaspaid:
            participanthaspaid.payment_request_id = payment_request_id
            participanthaspaid.save()
        # if there was no previous payment
        else:
            # transaction_id is set to be '-1' by default
            participanthaspaid = ParticipantHasPaid.objects.create(participant=participant,
                                                                   paid_event=event, payment_request_id=payment_request_id)
        return redirect(url)
    else:
        return HttpResponseServerError()


def weebhook(request):

    if request.method == "POST":
        data = request.POST.copy()
        mac_provided = data.pop('mac')[0]

        message = "|".join(v for k, v in sorted(
            data.items(), key=lambda x: x[0].lower()))
        mac_calculated = hmac.new(
            (os.getenv('PRIVATE_SALT')).encode('utf-8'), message.encode('utf-8'), hashlib.sha1).hexdigest()

        if mac_provided == mac_calculated:
            try:
                participantpaspaid = ParticipantHasPaid.objects.get(
                    payment_request_id=data['payment_request_id'])
                if data['status'] == "Credit":
                    # Payment was successful, mark it as completed in your database.
                    participantpaspaid.transaction_id = data['payment_id']
                    event=participantpaspaid.paid_event
                    ParticipantHasParticipated.objects.create(
                        participant=participant, event=event)
                    send_mail(
                        'Participation in ' + str(event.name) + ' in Zeitgeist 2k21',
                        'Dear ' + str(participant.name) + '\n\nThank you for participating in ' + str(event.name) + '. Please carry a Photo ID Proof with you for your onsite registration, otherwise your registration might get cancelled. We wish you best of luck. Give your best and stand a chance to win exciting prizes !!!\n\nReminder - Your PARTICIPANT CODE is ' + str(
                            participant.participant_code) + '. If you are also a Campus Ambassador for Zeitgeist 2k21, your PARTICIPANT CODE is also the same as your CAMPUS AMBASSADOR CODE.\n\nRegards\nZeitgeist 2k21 Public Relations Team',
                        'zeitgeist.pr@iitrpr.ac.in',
                        [participant.participating_user.email],
                        fail_silently=False,
                    )
                    # str(participantpaspaid.paid_event) inlcudes name of category also
                    send_mail(
                        'Payment confirmation of ' +
                        str(participantpaspaid.paid_event) +
                        ' to Zeitgeist 2k21',
                        'Dear ' + str(participantpaspaid.participant.name) + '\n\nThis is to confirm with you that your payment for the purpose, ' + str(participantpaspaid.paid_event) +
                        ', is successful.\n\nRegards\nZeitgeist 2k21 Public Relations Team',
                        'zeitgeist.pr@iitrpr.ac.in',
                        [participantpaspaid.participant.participating_user.email],
                        fail_silently=False,
                    )
                else:
                    # Payment was unsuccessful, mark it as failed in your database.
                    participantpaspaid.transaction_id = '0'
                participantpaspaid.save()
            except Exception as err:
                print(err)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)


def payment_redirect(request):

    return render(request, 'main_page/payment_details.html', {'payment_status': request.GET['payment_status'], 'payment_request_id': request.GET['payment_request_id'], 'payment_id': request.GET['payment_id']})


@login_required
def support(request):

    if request.method == 'POST':
        payable_amount = request.POST.get('amount')
        purpose = 'SUPPORT TO ZEITGEIST WORTH INR ' + str(payable_amount)
        response = support_payment_request(request.user.get_full_name(), payable_amount, purpose,
                        request.user.email, None)
        if response['success']:
            url = response['payment_request']['longurl']
            payment_request_id = response['payment_request']['id']
            Support.objects.create(donating_user=request.user, donation_amount=payable_amount, payment_request_id=payment_request_id)
            return redirect(url)
        else:
            return HttpResponseServerError()
    return render(request, 'main_page/support.html')


def support_weebhook(request):

    if request.method == "POST":
        data = request.POST.copy()
        mac_provided = data.pop('mac')[0]

        message = "|".join(v for k, v in sorted(
            data.items(), key=lambda x: x[0].lower()))
        mac_calculated = hmac.new(
            (os.getenv('PRIVATE_SALT')).encode('utf-8'), message.encode('utf-8'), hashlib.sha1).hexdigest()

        if mac_provided == mac_calculated:
            try:
                support = Support.objects.get(payment_request_id=data['payment_request_id'])
                if data['status'] == "Credit":
                    # Payment was successful, mark it as completed in your database.
                    support.transaction_id = data['payment_id']
                    # send_mail(
                    #     'Donation to Zeitgeist 2k21',
                    #     'Dear ' + str(request.user.get_full_name()) + '\n\nThank you for your donation to Zeitgeist 2k21. Awesome people like you are the main reason of success of Zeitgeist, and IIT Ropar as a whole. From the side of Zeitgeist 2k21 team, we thank you a lot for your valuable contribution.\n\nRegards\nZeitgeist 2k21 Public Relations Team',
                    #     'zeitgeist.pr@iitrpr.ac.in',
                    #     [request.user.email],
                    #     fail_silently=False,
                    # )
                else:
                    # Payment was unsuccessful, mark it as failed in your database.
                    support.transaction_id = '0'
                support.save()
            except Exception as err:
                print(err)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)


def support_payment_redirect(request):

    return render(request, 'main_page/payment_details.html', {'payment_status': request.GET['payment_status'], 'payment_request_id': request.GET['payment_request_id'], 'payment_id': request.GET['payment_id']})



def reach_us(request):

    return render(request, 'main_page/reach_us.html')


# --------------------------------------------------------------------------------------

def under_maintainance(request):

    return render(request, 'main_page/under_maintainance.html')





@staff_member_required
def send_email_all(request):

    participants = Participant.objects.all()
    emails = []

    for  participant in participants:
        emails.append(participant.participating_user.email)
    
    emails = list(set(emails))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="participant_emails.csv"'

    writer = csv.writer(response)

    for email in emails:

        writer.writerow([email])

    return response
