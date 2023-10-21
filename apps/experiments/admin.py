from django.contrib import admin

from apps.experiments.multiple_choice_models import MultipleChoiceQuestion, Stimulus
from apps.experiments.single_choice_models import SingleChoiceQuestion, SingleChoiceResult, SingleChoiceAnswer


@admin.register(SingleChoiceQuestion)
class SingleChoiceQuestionAdmin(admin.ModelAdmin):
    list_display = ('order', 'correct_sample', 'is_test_question', 'notes', 'created_at')


class AnswerInline(admin.TabularInline):
    model = SingleChoiceAnswer
    can_delete = False

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(SingleChoiceResult)
class SingleChoiceResultAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'notes']
    readonly_fields = ['created_at']
    inlines = [AnswerInline]


class StimulusInline(admin.StackedInline):
    model = Stimulus


@admin.register(MultipleChoiceQuestion)
class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    inlines = (StimulusInline,)
    list_display = ('order', 'created_at')
