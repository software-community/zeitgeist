from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class SubCategory(models.Model):

    name = models.CharField(max_length=40, null=False, blank=False)

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
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        null=False,
        blank=False,
    )

    participation_fees_per_person = models.IntegerField(blank=False)

    def __str__(self):
        return str(self.name) + " - " + str(self.category)

    class Meta:
        verbose_name_plural = 'Sub Categories'


class Event(models.Model):

    name = models.CharField(max_length=40, null=False, blank=False)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

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
    description = models.TextField(blank=False)

    def __str__(self):
        return str(self.name) + " - " + str(self.sub_category)


class Participant(models.Model):

    participating_user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile_number = PhoneNumberField(verbose_name='Mobile Number', region='IN')

    def __str__(self):
        return str(self.participating_user)


class ParticipantHasPaid(models.Model):

    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    paid_sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, default='-1')

    def __str__(self):
        return str(self.participant) + " - " + str(self.paid_sub_category)

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

    name = models.CharField(max_length=40, null=False, blank=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    captain = models.ForeignKey(Participant, on_delete=models.CASCADE)
    primary_mobile_number = PhoneNumberField(null=False, blank=False, verbose_name='Primary Mobile Number', region='IN')
    secondary_mobile_number = PhoneNumberField(null=False, blank=False, verbose_name='Secondary Mobile Number', region='IN')

    def __str__(self):
        return str(self.name) + " - " + str(self.event) + " - " + str(self.captain)


class TeamHasMember(models.Model):

    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    member = models.ForeignKey(Participant, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.team) + " - " + str(self.member)

    class Meta:
        verbose_name_plural = 'Team Has Member'
