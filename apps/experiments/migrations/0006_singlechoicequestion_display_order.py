# Generated by Django 4.2.6 on 2023-10-21 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0005_multiplechoiceresult_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='singlechoicequestion',
            name='display_order',
            field=models.PositiveIntegerField(default=0, verbose_name='Display order'),
        ),
    ]
