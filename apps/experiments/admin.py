from django.contrib import admin

from apps.experiments.multiple_choice_models import MultipleChoiceQuestion, Stimulus, MultipleChoiceResult, \
    MultipleChoiceAnswer
from apps.experiments.single_choice_models import SingleChoiceQuestion, SingleChoiceResult, SingleChoiceAnswer


@admin.register(SingleChoiceQuestion)
class SingleChoiceQuestionAdmin(admin.ModelAdmin):
    list_display = ('order', 'display_order', 'correct_sample', 'is_test_question', 'notes', 'created_at')
    list_filter = ('is_test_question',)


class SingleChoiceAnswerInline(admin.TabularInline):
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
    inlines = [SingleChoiceAnswerInline]


class StimulusInline(admin.StackedInline):
    model = Stimulus


@admin.register(MultipleChoiceQuestion)
class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    inlines = (StimulusInline,)
    list_display = ('order', 'created_at')


class MultipleChoiceAnswerInline(admin.TabularInline):
    model = MultipleChoiceAnswer
    can_delete = False
    fields = ['question_str', 'stimulus', 'selected_sample', 'response_time_ms']
    readonly_fields = ['question_str']

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('stimulus__question')


@admin.register(MultipleChoiceResult)
class MultipleChoiceResultAdmin(admin.ModelAdmin):
    inlines = [MultipleChoiceAnswerInline]
    list_display = ['created_at', 'notes']
