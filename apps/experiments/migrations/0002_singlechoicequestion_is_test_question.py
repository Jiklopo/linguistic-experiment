# Generated by Django 4.2.6 on 2023-10-21 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='singlechoicequestion',
            name='is_test_question',
            field=models.BooleanField(default=False, verbose_name='Is test question'),
        ),
    ]
