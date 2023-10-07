# Generated by Django 4.2.6 on 2023-10-07 17:46

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MultipleChoiceQuestion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('order', models.PositiveIntegerField(verbose_name='Order')),
                ('first_sample', models.FileField(upload_to='multiple_choice/first_samples', verbose_name='First sample')),
                ('second_sample', models.FileField(upload_to='multiple_choice/seconds_samples', verbose_name='Second sample')),
            ],
            options={
                'verbose_name': 'Multiple choice question',
                'verbose_name_plural': 'Multiple choice questions',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='SingleChoiceQuestion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('order', models.PositiveIntegerField(verbose_name='Order')),
                ('first_sample', models.FileField(upload_to='single_choice/first_samples', verbose_name='First sample')),
                ('second_sample', models.FileField(upload_to='single_choice/seconds_samples', verbose_name='Second sample')),
                ('stimulus', models.FileField(upload_to='single_choice/stimuli', verbose_name='Stimulus')),
            ],
            options={
                'verbose_name': 'Single choice question',
                'verbose_name_plural': 'Single choice questions',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Stimulus',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('order', models.PositiveIntegerField(verbose_name='Order')),
                ('file', models.FileField(upload_to='multiple_choice/stimuli', verbose_name='Audio file')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stimuli', to='experiments.multiplechoicequestion', verbose_name='Question')),
            ],
            options={
                'verbose_name': 'Stimulus',
                'verbose_name_plural': 'Stimuli',
                'ordering': ('order',),
            },
        ),
    ]