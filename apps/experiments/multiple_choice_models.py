from django.contrib import admin
from django.db import models

from apps.common.abstract_models import UUIDModel, DateTimeModel
from apps.experiments.choices import CorrectSampleChoices


class MultipleChoiceQuestion(UUIDModel, DateTimeModel):
    order = models.PositiveIntegerField('Order')
    first_sample = models.FileField('First sample', upload_to='multiple_choice/first_samples')
    second_sample = models.FileField('Second sample', upload_to='multiple_choice/seconds_samples')
    is_test_question = models.BooleanField('Is test question', default=False)

    def __str__(self):
        return f'Question #{self.order}'

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

    def __str__(self):
        return f'Stimulus #{self.order}'

    class Meta:
        verbose_name = 'Stimulus'
        verbose_name_plural = 'Stimuli'
        ordering = ('order',)


class MultipleChoiceResult(UUIDModel, DateTimeModel):
    notes = models.TextField('Notes', blank=True, null=True, help_text='Just notes for yourself')
    raw_json = models.JSONField(verbose_name='Raw JSON')

    def __str__(self):
        date_str = self.created_at.strftime('%d-%m-%Y %H:%M')
        return f'Result from {date_str}'

    class Meta:
        verbose_name = 'Multiple choice result'
        verbose_name_plural = 'Multiple choice results'
        ordering = ('-created_at',)


class MultipleChoiceAnswer(UUIDModel):
    result = models.ForeignKey(
        to=MultipleChoiceResult, on_delete=models.CASCADE,
        related_name='answers', verbose_name='Result'
    )
    stimulus = models.ForeignKey(
        to=Stimulus, on_delete=models.CASCADE,
        related_name='answers', verbose_name='Stimulus'
    )
    selected_sample = models.CharField(
        'Selected sample', max_length=1,
        choices=CorrectSampleChoices.choices
    )
    response_time_ms = models.PositiveIntegerField('Response time in ms')

    @property
    @admin.display(description='Question')
    def question_str(self) -> str:
        return str(self.stimulus.question)

    def __str__(self):
        return f'Answer Q{self.stimulus.question.order} | S{self.stimulus.order}'

    class Meta:
        verbose_name = 'Multiple choice answer'
        verbose_name_plural = 'Multiple choice answers'
        ordering = ('stimulus__question__order', 'stimulus__order')
