from django.contrib import admin

from apps.experiments.models import SingleChoiceQuestion, MultipleChoiceQuestion, Stimulus, SingleChoiceAnswer, \
    SingleChoiceResult


@admin.register(SingleChoiceQuestion)
class SingleChoiceQuestionAdmin(admin.ModelAdmin):
    list_display = ('order', 'notes', 'created_at')


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
    inlines = [AnswerInline]


class StimulusInline(admin.StackedInline):
    model = Stimulus


@admin.register(MultipleChoiceQuestion)
class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    inlines = (StimulusInline,)
    list_display = ('order', 'created_at')
