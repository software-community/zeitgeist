# Generated by Django 2.2.3 on 2019-09-30 22:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0018_auto_20190921_2117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accomodation',
            name='aadhar_no',
        ),
        migrations.RemoveField(
            model_name='accomodation',
            name='id',
        ),
        migrations.RemoveField(
            model_name='accomodation',
            name='no_of_days',
        ),
        migrations.AddField(
            model_name='accomodation',
            name='acco_for_day_one',
            field=models.BooleanField(default=False, verbose_name='11 Oct'),
        ),
        migrations.AddField(
            model_name='accomodation',
            name='acco_for_day_three',
            field=models.BooleanField(default=False, verbose_name='13 Oct'),
        ),
        migrations.AddField(
            model_name='accomodation',
            name='acco_for_day_two',
            field=models.BooleanField(default=False, verbose_name='12 Oct'),
        ),
        migrations.AlterField(
            model_name='accomodation',
            name='participant',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='main_page.Participant', verbose_name='Participant'),
        ),
    ]