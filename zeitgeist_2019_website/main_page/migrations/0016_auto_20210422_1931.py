# Generated by Django 2.2.3 on 2021-04-22 14:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0015_auto_20210422_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ongoingevents',
            name='end',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='ongoingevents',
            name='start',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='upcomingevents',
            name='end',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='upcomingevents',
            name='start',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]