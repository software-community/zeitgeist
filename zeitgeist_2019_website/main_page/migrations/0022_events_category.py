# Generated by Django 2.2.3 on 2021-03-23 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0021_remove_events_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_page.SubCat'),
        ),
    ]
