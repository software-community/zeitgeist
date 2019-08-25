# Generated by Django 2.2.3 on 2019-08-25 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0010_auto_20190825_0628'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aadhar_no', models.IntegerField(default=-1)),
                ('no_days', models.CharField(choices=[('ONE', '1 day'), ('TWO', '2 days'), ('THREE', '3 days')], max_length=10)),
                ('occupant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_page.Participant')),
            ],
        ),
    ]