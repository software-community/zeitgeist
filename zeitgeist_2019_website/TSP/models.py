from django.db import models
from django.forms import ModelForm
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

import os


class Profile(models.Model):
    school_name = models.CharField(max_length=150, blank=False)
    point_of_contact_name = models.CharField(max_length=50, blank=False)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 12 digits allowed.")
    # validators should be a list
    school_phone = models.CharField(
        validators=[phone_regex], max_length=12, blank=False)
    point_of_contact_phone = models.CharField(
        validators=[phone_regex], max_length=12, blank=False)
    school_address = models.TextField(blank=False)
    user = models.OneToOneField(User, related_name="TSP_user_profile", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name() + '\t' + self.school_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Payment(models.Model):
    profile = models.ForeignKey(Profile, on_delete = models.CASCADE)
    category_a = models.PositiveSmallIntegerField(verbose_name="No. of Students in Category A (Classes 9th & 10th)")
    category_b = models.PositiveSmallIntegerField(verbose_name="No. of Students in Category B (Classes 11th & 12th)")
    payment_request_id = models.CharField(max_length = 100, default = 'none')
    transaction_id = models.CharField(max_length=100, default='none')

    def __str__(self):
        return self.profile.user.get_full_name()

    def get_total_payment(self):
        category_a_fee = int(os.environ.get('CATEGORY_A_FEE', '50'))
        category_b_fee = int(os.environ.get('CATEGORY_B_FEE', '50'))

        return self.category_a*category_a_fee + self.category_b*category_b_fee
    
    def is_paid(self):
        if (self.transaction_id != 'none' and self.transaction_id != '0'
            and len(self.transaction_id) > 4):
            return True
        else:
            return False

class TSPResult(models.Model):
    advitiya_id = models.CharField(max_length = 10, blank=False)
    name = models.CharField(max_length = 50, blank=False)
    school = models.CharField(max_length = 50, blank=False)
    marks = models.SmallIntegerField(blank=False)
    rank = models.PositiveSmallIntegerField(blank=False)