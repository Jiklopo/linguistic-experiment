from django.contrib import admin

from apps.experiments.models import SingleChoiceQuestion, MultipleChoiceQuestion, Stimulus


@admin.register(SingleChoiceQuestion)
class SingleChoiceQuestionAdmin(admin.ModelAdmin):
    list_display = ('order', 'notes', 'created_at')


class StimulusInline(admin.StackedInline):
    model = Stimulus


@admin.register(MultipleChoiceQuestion)
class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    inlines = (StimulusInline,)
    list_display = ('order', 'created_at')
