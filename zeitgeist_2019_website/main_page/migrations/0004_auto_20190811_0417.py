# Generated by Django 2.2.3 on 2019-08-10 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0003_auto_20190811_0412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='category',
            field=models.CharField(choices=[('DC', 'Dance'), ('DM', 'Dramatics'), ('FA', 'Fine Arts'), ('GM', 'Gaming'), ('LS', 'Life Style'), ('LT', 'Literary'), ('MS', 'Music'), ('PH', 'Photography'), ('QZ', 'Quizzing'), ('VM', 'Video Making')], max_length=2),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
