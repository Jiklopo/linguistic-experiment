from django.db import models

from apps.common.abstract_models import UUIDModel, DateTimeModel


class SingleChoiceQuestion(UUIDModel, DateTimeModel):
    order = models.PositiveIntegerField('Order')
    first_sample = models.FileField('First sample', upload_to='single_choice/first_samples')
    second_sample = models.FileField('Second sample', upload_to='single_choice/seconds_samples')
    stimulus = models.FileField('Stimulus', upload_to='single_choice/stimuli')

    class Meta:
        verbose_name = 'Single choice question'
        verbose_name_plural = 'Single choice questions'
        ordering = ('order',)


class MultipleChoiceQuestion(UUIDModel, DateTimeModel):
    order = models.PositiveIntegerField('Order')
    first_sample = models.FileField('First sample', upload_to='multiple_choice/first_samples')
    second_sample = models.FileField('Second sample', upload_to='multiple_choice/seconds_samples')

    class Meta:
        verbose_name = 'Multiple choice question'
        verbose_name_plural = 'Multiple choice questions'
        ordering = ('order',)


class Stimulus(UUIDModel, DateTimeModel):
    question = models.ForeignKey(
        MultipleChoiceQuestion, on_delete=models.CASCADE,
        related_name='stimuli', verbose_name='Question'
    )
    order = models.PositiveIntegerField('Order')
    file = models.FileField('Audio file', upload_to='multiple_choice/stimuli')

    class Meta:
        verbose_name = 'Stimulus'
        verbose_name_plural = 'Stimuli'
        ordering = ('order',)
