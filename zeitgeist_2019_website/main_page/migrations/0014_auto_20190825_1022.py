# Generated by Django 2.2.3 on 2019-08-25 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0013_auto_20190825_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomregistration',
            name='aadhar_no',
            field=models.CharField(max_length=12, verbose_name='12-digit Aadhar No.'),
        ),
    ]