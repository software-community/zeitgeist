# Generated by Django 2.2.3 on 2019-08-17 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0002_auto_20190813_0258'),
    ]

    operations = [
        migrations.AddField(
            model_name='participanthaspaid',
            name='pay_request_id',
            field=models.CharField(default='-1', max_length=100),
        ),
    ]
