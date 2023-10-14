from django.db import models

from apps.common.abstract_models import UUIDModel, DateTimeModel
from apps.experiments.choices import CorrectSampleChoices


class SingleChoiceQuestion(UUIDModel, DateTimeModel):
    order = models.PositiveIntegerField('Order')
    first_sample = models.FileField('First sample', upload_to='single_choice/first_samples')
    second_sample = models.FileField('Second sample', upload_to='single_choice/seconds_samples')
    stimulus = models.FileField('Stimulus', upload_to='single_choice/stimuli')
    correct_sample = models.IntegerField(
        'Correct sample',
        choices=CorrectSampleChoices.choices,
        default=CorrectSampleChoices.FIRST
    )

    notes = models.TextField('Notes', blank=True, null=True, help_text='Just notes for yourself')

    class Meta:
        verbose_name = 'Single choice question'
        verbose_name_plural = 'Single choice questions'
        ordering = ('order',)


class SingleChoiceResult(UUIDModel, DateTimeModel):
    notes = models.TextField('Notes', blank=True, null=True, help_text='Just notes for yourself')

    class Meta:
        verbose_name = 'result'
        verbose_name_plural = 'results'
        ordering = ('-created_at',)


class SingleChoiceAnswer(UUIDModel):
    result = models.ForeignKey(
        SingleChoiceResult, on_delete=models.CASCADE,
        related_name='answers', verbose_name='Result'
    )
    question = models.ForeignKey(
        SingleChoiceQuestion, on_delete=models.CASCADE,
        related_name='answers', verbose_name='Question'
    )
    selected_sample = models.IntegerField('Selected sample', choices=CorrectSampleChoices.choices)
    is_correct = models.BooleanField('Is correct')

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
        ordering = ('-result__created_at', 'question__order')


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
