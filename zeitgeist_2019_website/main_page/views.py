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
from .methods import payment_request, accomodation_payment_request
from django.forms import formset_factory
# from django.contrib import messages
# Create your views here.


def main_page_home(request):
    sponsors = Sponsor.objects.all()
    context={'title': 'Zeitgeist', 'sponsors': sponsors}
    return render(request, 'main_page/index.html',context)


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
        prev_participant_registration_details = Participant.objects.get(participating_user=request.user)
    except Participant.DoesNotExist:
        prev_participant_registration_details = None

    if prev_participant_registration_details:
        messages={'1':'You are already registered as Participant','4':'If you want to edit your response, please contact:'}
        buttons=[{'link':'tel:7742522607','text':'7742522607'}]
        return render(request, 'main_page/messages.html', context={'messages':messages,'buttons':buttons})

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
            #     'Welcome to Zeitgeist 2k19',
            #     'Dear ' + str(new_participant_registration.name) + '\n\nThank you for showing your interest in Zeitgeist 2k19. We are excited for your journey with us and wish you luck for all the events that you take part in.\n\nYour PARTICIPANT CODE is ' + str(
            #         new_participant_registration.participant_code) + '. If you are also a Campus Ambassador for Zeitgeist 2k19, your PARTICIPANT CODE is also the same as your CAMPUS AMBASSADOR CODE.\n\nNote that this email is not for your participation in any event. To participate in events, you need to register for them on the Events page of Zeitgeist website. We wish you best of luck. Give your best and stand a chance to win exciting prizes !!!\n\nRegards\nZeitgeist 2k19 Public Relations Team',
            #     'zeitgeist.pr@iitrpr.ac.in',
            #     [new_participant_registration.participating_user.email],
            #     fail_silently=False,
            # )
            messages={'2':f'You have registered yourself successfully as a participant. Your PARTICIPANT CODE is {request.user.participant.participant_code }.','4':f'If you are also a Campus Ambassador for Zeitgeist 2k19, your PARTICIPANT CODE is also the same as your CAMPUS AMBASSADOR CODE. You must use this code for participating in any event in Zeitgeist 2k19. We have also emailed this code to your email address { request.user.email }.','1':' Note that this message is not for your participation in any event. To participate in events, you need to register for them on the Events page. We wish you best of luck for all the events you take part in. Give your best and stand a chance to win exciting prizes !!!'}
            return render(request, 'main_page/messages.html',{'messages':messages})
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
        participant = Participant.objects.get(participating_user=request.user)
    except Participant.DoesNotExist:
        return redirect('register_as_participant')

    event = Event.objects.get(id=event_id)

    try:
        ParticipantHasParticipated.objects.get(participant=participant, event=event)
        # code did not blow, hence participant has already participated in this event
        messages={'2':"You have already registered for this event! Double participation for one event is not allowed."}
        return render(request, 'main_page/messages.html', {'messages':messages})
    except:
        pass

    if event.event_type == 'Solo':
        try:
            payment_details = ParticipantHasPaid.objects.get(participant=participant, paid_subcategory=event.subcategory)
            if payment_details.transaction_id == '-1' or payment_details.transaction_id == '0':
                return redirect('pay_for_subcategory', subcategory_id=event.subcategory.id)
        except ParticipantHasPaid.DoesNotExist:
            return redirect('pay_for_subcategory', subcategory_id=event.subcategory.id)
        ParticipantHasParticipated.objects.create(participant=participant, event=event)
        send_mail(
            'Participation in ' + str(event.name) + ' in Zeitgeist 2k19',
            'Dear ' + str(participant.name) + '\n\nThank you for participating in ' + str(event.name) + '. Please carry a Photo ID Proof with you for your onsite registration, otherwise your registration might get cancelled. We wish you best of luck. Give your best and stand a chance to win exciting prizes !!!\n\nReminder - Your PARTICIPANT CODE is ' + str(
                participant.participant_code) + '. If you are also a Campus Ambassador for Zeitgeist 2k19, your PARTICIPANT CODE is also the same as your CAMPUS AMBASSADOR CODE.\n For Accomodation visit https://zeitgesit.org.in/accomodation \n\nRegards\nZeitgeist 2k19 Public Relations Team',
            'zeitgeist.pr@iitrpr.ac.in',
            [participant.participating_user.email],
            fail_silently=False,
        )
        messages={'1':f'Your Registration for the event {event.name} is succesfull.','2': 'Please carry a Photo ID Proof with you for your onsite registration, otherwise your registration might get cancelled. We wish you best of luck.'}
        return render(request, 'main_page/messages.html', context={'messages':messages})

    else:
        TeamHasMemberFormSet = formset_factory(form=TeamHasMemberForm, formset=BaseTeamFormSet, extra=event.maximum_team_size-1, max_num=event.maximum_team_size, validate_max=True, min_num=event.minimum_team_size, validate_min=True)
        if request.method == "POST":
            list_of_team_members = []
            list_of_email_addresses_of_team_members = []
            team_member_formset = TeamHasMemberFormSet(request.POST, initial=[{'team_member' : str(participant.participant_code)}], prefix='team_member')
            team_form = TeamForm(request.POST)
            if team_member_formset.is_valid() and team_form.is_valid():
                for team_member_form in team_member_formset:
                    team_member = team_member_form.cleaned_data.get('team_member')
                    # if form was empty
                    if not team_member:
                        continue
                    list_of_team_members.append(team_member)
                    list_of_email_addresses_of_team_members.append(team_member.participating_user.email)
                    # since participant is already validated, his model must exist
                    try:
                        team_member_payment = ParticipantHasPaid.objects.get(participant=team_member, paid_subcategory=event.subcategory)
                        if team_member_payment.transaction_id == '-1' or team_member_payment.transaction_id == '0':
                            messages={'1':"Some of the team members have not paid for the subcategory !!!",'2':"Try again when all the team members have paid for the subcategory."}
                            return render(request,'main_page/messages.html',context={'messages':messages })
                    except ParticipantHasPaid.DoesNotExist:
                        messages={'1':"Some of the team members have not paid for the subcategory !!!",'2':"Try again when all the team members have paid for the subcategory."}
                        return render(request,'main_page/messages.html',context={'messages':messages})
                # print(team_form.cleaned_data)
                new_team = team_form.save(commit=False)
                temp_team_code = str(request.user.id) + datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
                new_team.team_code = temp_team_code
                new_team.event = event
                new_team.captain = participant
                new_team.save()
                new_team = Team.objects.get(team_code=temp_team_code)
                new_team_code = ((str(new_team.name).replace(" ", ""))[:4]).upper() + str(new_team.id) + 'Z19'
                new_team.team_code = new_team_code
                new_team.save()
                new_team = Team.objects.get(team_code=new_team_code)
                for team_member in list_of_team_members:
                    ParticipantHasParticipated.objects.create(participant=team_member, event=event)
                    TeamHasMember.objects.create(team=new_team, member=team_member)
                send_mail(
                    'Participation in ' + str(event.name) + ' in Zeitgeist 2k19',
                    'Dear ' + str(new_team.name) + '\n\nThank you for participating in ' + str(event.name) + '. Each of you must carry a Photo ID Proof with you for your onsite registration, otherwise your registration might get cancelled.\n\nYour TEAM CODE is ' + str(new_team.team_code) + '. We wish you best of luck. Give your best and stand a chance to win exciting prizes !!!\n For Accomodation visit https://zeitgeist.org.in/accomodation \n\nRegards\nZeitgeist 2k19 Public Relations Team',
                    'zeitgeist.pr@iitrpr.ac.in',
                    list_of_email_addresses_of_team_members,
                    fail_silently=False,
                )
                messages={'1':f"Your Registration for the event {event.name} is succesfull.",'2':f'Your TEAM CODE is: {new_team_code}. Each of you must carry a Photo ID Proof with you for your onsite registration, otherwise your registration might get cancelled. We wish you best of luck.'}
                return render(request, 'main_page/messages.html', context={'messages':messages  })
        else:
            team_form = TeamForm()
            team_member_formset = TeamHasMemberFormSet(initial=[{'team_member' : str(participant.participant_code)}], prefix='team_member')

        return render(request, 'main_page/register_team.html',
                        {   'event': event,
                            'team_form': team_form,
                            'team_member_formset': team_member_formset,
                            })


@login_required
def pay_for_subcategory(request, subcategory_id):

    try:
        participant = Participant.objects.get(participating_user=request.user)
    except:
        return redirect('register_as_participant')

    subcategory = Subcategory.objects.get(id=subcategory_id)

    try:
        ParticipantHasPaid.objects.get(participant=participant, paid_subcategory=subcategory)
        messages={'1':'You have already paid for this Subcategory','2':'You do not need to pay again.'}
        # code did not blow, hence participant has already paid for this subcategory
        return render(request,'main_page/messages.html',context={'messages':messages})
    except:
        pass

    purpose = 'PAYMENT FOR ' + str(subcategory.name).upper() + ' OF ' + str(subcategory.category.name).upper() + ' CATEGORY'
    response = payment_request(participant.name, subcategory.participation_fees_per_person, purpose,
                request.user.email, participant.contact_mobile_number.__str__())

    if response['success']:
        url = response['payment_request']['longurl']
        payment_request_id = response['payment_request']['id']
        participanthaspaid = ParticipantHasPaid.objects.create(participant=participant,
                                                               paid_subcategory=subcategory, payment_request_id=payment_request_id)
        return redirect(url)
    else:
        return HttpResponseServerError()


def weebhook(request):

    if request.method == "POST":
        # print(request.POST)
        data = request.POST.copy()
        mac_provided = data.pop('mac')[0]

        message = "|".join(v for k, v in sorted(
            data.items(), key=lambda x: x[0].lower()))
        mac_calculated = hmac.new(
            (os.getenv('private_salt')).encode('utf-8'), message.encode('utf-8'), hashlib.sha1).hexdigest()

        if mac_provided == mac_calculated:
            try:
                participantpaspaid = ParticipantHasPaid.objects.get(
                    payment_request_id=data['payment_request_id'])
                if data['status'] == "Credit":
                    # Payment was successful, mark it as completed in your database.
                    participantpaspaid.transaction_id = data['payment_id']
                    # str(participantpaspaid.paid_subcategory) inlcudes name of category also
                    send_mail(
                        'Payment confirmation of ' + str(participantpaspaid.paid_subcategory) + ' to Zeitgeist 2k19',
                        'Dear ' + str(participantpaspaid.participant.name) + '\n\nThis is to confirm with you that your payment for the purpose, ' + str(participantpaspaid.paid_subcategory) + ', is successful. However, this does not mean you have participated in an event of that subcategory, it only means that you are now eligible to register for any event in that subcategory. To participate in an event of the subcategory you have paid for, you need to register for that event on the Zeitgeist website. For every event you take part in, you will receive an email comfirming your participation in that event.\n\nRegards\nZeitgeist 2k19 Public Relations Team',
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
    participanthaspaid=ParticipantHasPaid.objects.get(payment_request_id=request.GET['payment_request_id'])
    paidsubcategory=participanthaspaid.paid_subcategory
    if participanthaspaid.transaction_id == '-1' or participanthaspaid.transaction_id=='0':
        mp=['Payment Status : '+request.GET['payment_status'],'Payment Request ID : '+ request.GET['payment_request_id']]
        messages={'1':'Your Payment was unsuccesfull.'}
    else :
        mp=['Transaction ID :'+ request.GET['payment_id'],'Payment Status : '+request.GET['payment_status'],'Payment Request ID : '+ request.GET['payment_request_id']]
        messages={
            '4':'Your payment for the purpose, ' + str(paidsubcategory) + ', is successful. However, this does not mean you have participated in an event of that subcategory. It only means that you are now eligible to register for any event in that subcategory . To participate in an event of the subcategory you have paid for, you need to register for that event on the Zeitgeist website. For every event you take part in, you will receive an email comfirming your participation in that event.'}
    return render(request,'main_page/messages.html',{'messages':messages,'mp':mp})


@login_required
def accomodation(request):
    try:
        participant=Participant.objects.get(participating_user=request.user)
        
        participantdata=ParticipantHasParticipated.objects.filter(participant=participant)
        # print(participantdata)
        #we will give accomodation if he has participated in atleast one event
        if len(participantdata)== 0:
            
            raise ParticipantHasParticipated.DoesNotExist('no query')
    except:
        messages={'1':'You can view this page only if you have participated in an event'}
        return render(request,'main_page/messages.html',{'messages':messages})
    try:
        accomodation=Accomodation.objects.get(participant=participant)
        #checking if he has alredy booked or his transaction failed
        if accomodation.transaction_id == '0' or accomodation.transaction_id == '-1':
            #transaction failed case
            #redirect to payment page
            return redirect('accomodation_pay')
        else :
            #booking already case 
            messages={'1':'You can book only Once'}
            return render(request,'main_page/messages.html',{'messages':messages})
    except:
        pass
    
    if request.method=='POST':
        accomodationform=AccomodationForm(request.POST)
        if accomodationform.is_valid():
            accomodation=accomodationform.save(commit=False)
            accomodation.participant=participant
            accomodation.save()
            return redirect('accomodation_pay')
            # messages={'1':'Request Submitted Succesfully','2':'Please carry your Aadhar Card for verification of identity','3':'Please complete your payment below'}
            # buttons=[{'link':'{%  %}'}]
            # return render(request,'main_page/messages.html',{'messages':messages})
    else:
        accomodationform=AccomodationForm()
    
    charges={'1':300,'2':500,'3':700}
    return render(request,'main_page/accomodate.html',{'form':accomodationform,'charges':charges})


@login_required
def accomodation_payment(request):
    try:
        participant = Participant.objects.get(participating_user=request.user)
    except:
        return redirect('register_as_participant')
    try:
        accomodation=Accomodation.objects.get(participant=participant)
        
    except:
        messages={'1':'Sorry, You are at the Worng Place'}
        return render(request,'main_page/messages.html',{'messages':messages})
    # print(accomodation.no_days)
    # subcategory = Subcategory.objects.get(id=subcategory_id)

    # try:
    #     ParticipantHasPaid.objects.get(participant=participant, paid_subcategory=subcategory)
    #     messages={'1':'You have already paid for this Subcategory','2':'You do not need to pay again.'}
    #     # code did not blow, hence participant has already paid for this subcategory
    #     return render(request,'main_page/messages.html',context={'messages':messages})
    # except:
    #     pass

    charges={'1':300,'2':500,'3':700}
    purpose = 'PAYMENT FOR ACCOMODATION FOR '+str(accomodation.no_days)
    response = accomodation_payment_request(participant.name,charges[str(accomodation.no_days)], purpose,
                request.user.email, participant.contact_mobile_number.__str__())

    if response['success']:
        url = response['payment_request']['longurl']
        payment_request_id = response['payment_request']['id']
        
        accomodation.payment_request_id=payment_request_id
        accomodation.save()
        return redirect(url)
    else:
        return HttpResponseServerError()

def accomodation_weebhook(request):
    
    if request.method == "POST":
        # print(request.POST)
        data = request.POST.copy()
        mac_provided = data.pop('mac')[0]

        message = "|".join(v for k, v in sorted(
            data.items(), key=lambda x: x[0].lower()))
        mac_calculated = hmac.new(
            (os.getenv('private_salt')).encode('utf-8'), message.encode('utf-8'), hashlib.sha1).hexdigest()

        if mac_provided == mac_calculated:
            try:
                accomodation = Accomodation.objects.get(
                    payment_request_id=data['payment_request_id'])
                if data['status'] == "Credit":
                    # Payment was successful, mark it as completed in your database.
                    accomodation.transaction_id = data['payment_id']
                else:
                    # Payment was unsuccessful, mark it as failed in your database.
                    accomodation.transaction_id = '0'
                accomodation.save()
            except Exception as err:
                print(err)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)

def accomodation_payment_redirect(request):
    accomodation=Accomodation.objects.get(payment_request_id=request.GET['payment_request_id'])
    if accomodation.transaction_id =='-1' or accomodation.transaction_id=='0':
        mp=['Payment Status : '+request.GET['payment_status'],'Payment Request ID : '+ request.GET['payment_request_id']]
        messages={'1':'  Payment Status: '+request.GET['payment_status']+'  Payment Request ID: '+request.GET['payment_request_id'],'2':'Please try again'}
    else:
        mp=['Transaction ID :'+ request.GET['payment_id'],'Payment Status : '+request.GET['payment_status'],'Payment Request ID : '+ request.GET['payment_request_id']]
        messages={'2':'Please bring your aadhar card for verification purposes.'}
    return render(request,'main_page/messages.html',{'messages':messages,'mp':mp})

# def testing(request):
#     mp=['Hello','I am here','what about you!!']
#     return render(request,'main_page/messages.html',{'mp':mp})