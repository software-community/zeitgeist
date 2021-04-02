# Generated by Django 2.2.3 on 2021-04-02 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0004_ourteam'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('mobile', models.CharField(max_length=100)),
                ('organization', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('z_code', models.CharField(max_length=100)),
                ('events', models.CharField(max_length=5000)),
                ('total', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Registrations',
            },
        ),
    ]