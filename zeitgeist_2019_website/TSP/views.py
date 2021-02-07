from django.shortcuts import render, redirect
from django.conf.urls import include
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponse
from django.contrib.auth.decorators import user_passes_test 

import os
import hashlib
import hmac

from TSP import models
from TSP.forms import registerForm, PaymentForm, ResultForm
from TSP.methods import get_paid_details, payment_request


def home(request):
    person = True
    return render(request, 'TSP/index.html', {'person': person})

def result_view(request):
    form = ResultForm(request.POST or None)
    if(request.method == 'POST'):
        if form.is_valid():
            advitiya_id = form.cleaned_data['advitiya_id']
            name = form.cleaned_data['name']
            try:
                data = models.TSPResult.objects.filter(
                    name__icontains=name, advitiya_id=advitiya_id)[0]
                if data.marks == -100:
                    form.add_error(None, error='You didn\'t appear for the test')
                else:
                    return render(request, "TSP/result_view.html", { 'data' : data})
            except:
                form.add_error(None, error='Result Not Found')
    return render(request, "TSP/result.html", { 'form' : form})

@login_required(login_url='/auth/google/login/')
def register_profile(request):
    person = models.Profile.objects.filter(user=request.user)
    if(person.count()):
        return redirect('TSP:profile')
    else:
        form = registerForm(request.POST or None)
    if(request.method == 'POST'):
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            send_mail(subject='Successful Registration for Techno School program: Zeitgeist 2020',
                      message='',
                      from_email=os.environ.get(
                          'EMAIL_HOST_USER', ''),
                      recipient_list=[instance.user.email],
                      fail_silently=True,
                      html_message='Dear ' + str(request.user.get_full_name()) +
                      ',<br><br>You are successfully registered for Techno School program for Zeitgeist 2020.' +
                      'We are excited for your journey with us.' +
                      '<br>Please read the <b>TSP Brochure</b> at https://'
                      + request.get_host() + static('TSP/TSP_Invitation.pdf') + '<br><br>For any queries, feel free to contact Mr. Akash(8949852311), or Mr. Jishu(9110914050)<br><br>Regards<br>Zeitgeist 2020 ' +
                      '<br>Public Relations Team')
            return redirect('TSP:profile')
    return render(request, "TSP/register.html", {"form": form, 'person': person})


@login_required(login_url='/auth/google/login/')
def profile(request):
    user = request.user
    try:
        person = models.Profile.objects.get(user=user)
        num_cat_a, num_cat_b =get_paid_details(person)
        context = {
            "profile": person,
            "num_cat_a": num_cat_a,
            "num_cat_b": num_cat_b,
        }
        return render(request, "TSP/profile.html", context=context)
    except:
        return redirect('TSP:register_profile')

@login_required(login_url='/auth/google/login/')
def fee_payment(request):

    try:
        person = models.Profile.objects.get(user=request.user)
    except Exception as err:
        print(err)
        return redirect('TSP:register_profile')

    form = PaymentForm(request.POST or None)

    num_cat_a, num_cat_b = get_paid_details(person)

    if(request.method == 'POST'):
        if form.is_valid():
            payment_instance = form.save(commit=False)
            payment_instance.profile = person

            purpose = "Registration Fee for TSP"
            response = payment_request(request.user.get_full_name(), payment_instance.get_total_payment(),
                    purpose, request.user.email, str(person.school_phone))

            if response['success']:
                url = response['payment_request']['longurl']
                payment_request_id = response['payment_request']['id']
                payment_instance.payment_request_id = payment_request_id
                payment_instance.save()
                return redirect(url)
            else:
                print(response)
                return HttpResponseServerError()

    return render(request, "TSP/payment.html", {'form': form, "num_cat_a": num_cat_a,
                             "num_cat_b": num_cat_b, "person": person})

def webhook(request):

    if request.method == "POST":
        data = request.POST.copy()
        mac_provided = data.pop('mac')[0]

        message = "|".join(v for k, v in sorted(
            data.items(), key=lambda x: x[0].lower()))
        mac_calculated = hmac.new(
            (os.getenv('PRIVATE_SALT')).encode('utf-8'), message.encode('utf-8'), hashlib.sha1).hexdigest()

        if mac_provided == mac_calculated:
            try:
                payment_detail = models.Payment.objects.get(
                    payment_request_id=data['payment_request_id'])
                if data['status'] == "Credit":
                    # Payment was successful, mark it as completed in your database.
                    payment_detail.transaction_id = data['payment_id']
                    # str(participantpaspaid.paid_subcategory) inlcudes name of category also
                    send_mail(
                        'Payment confirmation of TSP | ZEITGEIST 2k21',
                        'Dear ' + str(payment_detail.profile.user.get_full_name()) + '\n\nThis is to confirm '+
                        'that your payment to ZEITGEIST 2k21 ' +
                        ' is successful.\n\n'+
                        'No. of Students in Category A(9-10th class) : '+ str(payment_detail.category_a) +
                        '\nNo. of Students in Category B(11-12th class) : '+ str(payment_detail.category_b) +
                        '\n Total Payment of Rs. ' + str(payment_detail.get_total_payment()) +
                        '\n\nRegards\nZEITGEIST 2k21 Public Relations Team',
                        os.environ.get(
                          'EMAIL_HOST_USER', ''),
                        [payment_detail.profile.user.email],
                        fail_silently=True,
                    )
                else:
                    # Payment was unsuccessful, mark it as failed in your database.
                    payment_detail.transaction_id = '0'
                payment_detail.save()
            except Exception as err:
                print(err)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)


def payment_redirect(request):
    
    retry_for_payment = '<a href="'+reverse('TSP:profile')+'">Go Back</a>'

    return render(request, 'main_page/show_info.html',
            {
                'message': "<p><b>Payment Status:</b> " + request.GET['payment_status'] +
                            "</p><p><b>Payment Request ID:</b> " + request.GET['payment_request_id'] +
                            "</p><p><b>Payment Transaction ID:</b> " + request.GET['payment_id'] +
                            "<p>" + retry_for_payment + "</p>"
            })

import csv 
from django.http import HttpResponse

@user_passes_test(lambda u: u.is_superuser)
def upload_tsp_data(request):
    added = 0
    failed = ''
    already = 0
    with open('tsp_data.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            advitiya_id = row[0]
            try:
                _, created = models.TSPResult.objects.get_or_create(
                        advitiya_id = advitiya_id,
                        defaults={
                            'name': row[1],
                            'school' : row[2],
                            'marks' : row[3],
                            'rank' : row[4]
                            }
                    )
                if created:
                    added = added + 1
                else:
                    already = already + 1
            except:
                if advitiya_id == None:
                    advitiya_id = 'not found'
                failed = failed + ' ' + advitiya_id
    return HttpResponse('Added : ' + str(added) + ' Already : ' + str(already) + 
                        ' Failed : ' + str(failed))
    