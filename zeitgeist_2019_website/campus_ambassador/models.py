from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class RegistrationDetails(models.Model):
    college = models.CharField(max_length=200)
    # would have liked to use PhoneNumberField from phonenumber_field.modelfields
    # pip install django-phonenumber-field
    # pip install phonenumbers (or) pip install phonenumberslite
    mobile_number = models.CharField(max_length=15)
    why_interested = models.TextField()
    past_experience = models.TextField()
    accept_campus_ambassador_policy = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        verbose_name_plural = 'Registration details'

    def __str__(self):
        return 'Registration by ' + str(self.user)
