from django.db import models

from apps.common.abstract_models import UUIDModel, DateTimeModel
from apps.experiments.choices import CorrectSampleChoices


class SingleChoiceQuestion(UUIDModel, DateTimeModel):
    order = models.PositiveIntegerField('Order')
    display_order = models.PositiveIntegerField('Display order', default=0)
    first_sample = models.FileField('First sample', upload_to='single_choice/first_samples')
    second_sample = models.FileField('Second sample', upload_to='single_choice/seconds_samples')
    stimulus = models.FileField('Stimulus', upload_to='single_choice/stimuli')
    correct_sample = models.CharField(
        'Correct sample', max_length=1,
        choices=CorrectSampleChoices.choices
    )
    is_test_question = models.BooleanField('Is test question', default=False)
    notes = models.TextField('Notes', blank=True, null=True, help_text='Just notes for yourself')

    def __str__(self):
        return f'Question #{self.order}'

    class Meta:
        verbose_name = 'Single choice question'
        verbose_name_plural = 'Single choice questions'
        ordering = ('order',)


class SingleChoiceResult(UUIDModel, DateTimeModel):
    notes = models.TextField('Notes', blank=True, null=True, help_text='Just notes for yourself')
    raw_json = models.JSONField(verbose_name='Raw JSON')

    def __str__(self):
        date_str = self.created_at.strftime('%d-%m-%Y %H:%M')
        return f'Result from {date_str}'

    class Meta:
        verbose_name = 'Single choice result'
        verbose_name_plural = 'Single choice results'
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
    selected_sample = models.CharField(
        'Selected sample', max_length=1,
        choices=CorrectSampleChoices.choices
    )
    response_time_ms = models.PositiveIntegerField('Response time in ms')
    is_correct = models.BooleanField('Is correct')

    def __str__(self):
        return f'Answer #{self.question.order}'

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
        ordering = ('-result__created_at', 'question__order')


class SingleChoiceExport(UUIDModel, DateTimeModel):
    notes = models.TextField('Notes', blank=True, null=True, help_text='Just notes for yourself')
    export_file = models.FileField('Export file', upload_to='results/single_choice', )

    class Meta:
        verbose_name = 'Single choice export'
        verbose_name_plural = 'Single choice exports'
        ordering = ('-created_at',)
