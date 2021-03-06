# Generated by Django 2.2.3 on 2019-08-25 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0011_sponsor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accomodation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(default='-1', max_length=100)),
                ('payment_request_id', models.CharField(default='-1', max_length=100)),
                ('aadhar_no', models.CharField(max_length=4, verbose_name='Last 4 digits of Aadhar No.')),
                ('no_days', models.CharField(choices=[('1', '1 day'), ('2', '2 days'), ('3', '3 days')], max_length=10, verbose_name='No. of days')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_page.Participant')),
            ],
            options={
                'verbose_name_plural': 'Accomodation',
            },
        ),
    ]
