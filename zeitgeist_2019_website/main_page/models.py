from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from campus_ambassador.models import *

# Create your models here.


class Category(models.Model):
    
    CATEGORY_CHOICES = [
        ('Dance', 'Dance'),
        ('Dramatics', 'Dramatics'),
        ('Fine Arts', 'Fine Arts'),
        ('Gaming', 'Gaming'),
        ('Life Style', 'Life Style'),
        ('Literary', 'Literary'),
        ('Music', 'Music'),
        ('Photography', 'Photography'),
        ('Quizzing', 'Quizzing'),
        ('Video Making', 'Video Making'),
    ]
    name = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        null=False,
        blank=False,
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = 'Categories'


class Subcategory(models.Model):

    name = models.CharField(max_length=40, null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False)
    participation_fees_per_person = models.IntegerField(blank=False)

    def __str__(self):
        return str(self.name) + " - " + str(self.category)

    class Meta:
        verbose_name_plural = 'Subcategories'


class Event(models.Model):

    name = models.CharField(max_length=40, null=False, blank=False)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

    EVENT_TYPE_CHOICES = [
        ('Solo', 'Solo'),
        ('Duet', 'Duet'),
        ('Group', 'Group'),
    ]
    event_type = models.CharField(
        max_length=5,
        choices=EVENT_TYPE_CHOICES,
        null=False,
        blank=False,
    )

    first_cash_prize = models.IntegerField(blank=False)
    second_cash_prize = models.IntegerField(blank=False)
    third_cash_prize = models.IntegerField(blank=False)
    minimum_team_size = models.IntegerField(blank=False)
    maximum_team_size = models.IntegerField(blank=False)
    start_date_time = models.DateTimeField(blank=False)
    end_date_time = models.DateTimeField(blank=False)
    link_to_rulebook = models.URLField(max_length=400, verbose_name='Link to Rulebook', blank=False)
    description = models.TextField(blank=False)

    def __str__(self):
        return str(self.name) + " - " + str(self.subcategory)


class Participant(models.Model):

    participating_user = models.OneToOneField(User, verbose_name='Participating User', on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(verbose_name='Name', max_length=40, null=False, blank=False)
    participant_code = models.CharField(max_length=15, verbose_name='Participant Code', unique=True)
    college = models.CharField(max_length=200, verbose_name='College Name')
    mobile_number = PhoneNumberField(null=False, blank=False, verbose_name='Mobile Number', region='IN')
    referring_ca = models.ForeignKey(RegistrationDetails, verbose_name='CA Referral Code', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.participant_code)


class ParticipantHasPaid(models.Model):

    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    paid_subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, default='-1')
    payment_request_id = models.CharField(max_length=100, default='-1')

    def __str__(self):
        return str(self.participant) + " - " + str(self.paid_subcategory)

    class Meta:
        verbose_name_plural = 'Participant Has Paid'


class ParticipantHasParticipated(models.Model):

    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.participant) + " - " + str(self.event)

    class Meta:
        verbose_name_plural = 'Participant Has Participated'


class Team(models.Model):

    name = models.CharField(max_length=40, verbose_name='Team Name', null=False, blank=False)
    team_code = models.CharField(max_length=15, verbose_name='Team Code', unique=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    captain = models.ForeignKey(Participant, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.team_code) + " - " + str(self.name)


class TeamHasMember(models.Model):

    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    member = models.ForeignKey(Participant, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.team) + " - " + str(self.member)

    class Meta:
        verbose_name_plural = 'Team Has Member'
