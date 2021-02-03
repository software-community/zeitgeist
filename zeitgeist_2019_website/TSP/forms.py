from django import forms
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re
from TSP.models import Profile, Payment


phone_re = re.compile(r'[0-9]{10,10}')
phone_validator = RegexValidator(regex=phone_re, message='Invalid phone number')

class registerForm(forms.ModelForm):
    school_phone = forms.CharField(required = True, label = 'School Phone',validators= [phone_validator],widget=forms.TextInput)
    school_name=forms.CharField(label="School Name",widget=forms.TextInput)
    school_address=forms.CharField(label="School Address",widget=forms.Textarea)
    point_of_contact_name=forms.CharField(label="Point of Contact Name",widget=forms.TextInput)
    point_of_contact_phone = forms.CharField(required = True, label = 'Point of Contact Phone',validators= [phone_validator],widget=forms.TextInput)
    class Meta:
        model= Profile
        fields=["school_name","school_address","school_phone","point_of_contact_name","point_of_contact_phone"]

class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields=["category_a", "category_b"]

class ResultForm(forms.Form):
    name = forms.CharField(label="Your Name", min_length=4,widget=forms.TextInput)
    advitiya_id = forms.CharField(label="Advitiya ID",widget=forms.TextInput)
