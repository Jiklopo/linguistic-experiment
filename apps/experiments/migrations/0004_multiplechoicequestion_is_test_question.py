# Generated by Django 4.2.6 on 2023-10-21 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0003_alter_singlechoiceanswer_selected_sample_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='is_test_question',
            field=models.BooleanField(default=False, verbose_name='Is test question'),
        ),
    ]
