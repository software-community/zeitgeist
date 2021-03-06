# Generated by Django 2.2.3 on 2019-07-09 21:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationDetails',
            fields=[
                ('college', models.CharField(max_length=200)),
                ('mobile_number', models.CharField(max_length=15)),
                ('why_interested', models.TextField()),
                ('past_experience', models.TextField()),
                ('accept_campus_ambassador_policy', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Registration details',
            },
        ),
    ]
