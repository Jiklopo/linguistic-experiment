from django.db.models import Prefetch
from django.views import generic
from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.experiments.multiple_choice_models import MultipleChoiceQuestion, MultipleChoiceResult
from apps.experiments.serializers import SingleChoiceResultSerializer, MultipleChoiceResultSerializer
from apps.experiments.single_choice_models import SingleChoiceQuestion, SingleChoiceResult


class SingleChoiceExperimentView(generic.TemplateView):
    template_name = 'experiments/single_choice.html'

    @staticmethod
    def split_list(input_list, chunk_size):
        return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_qs = SingleChoiceQuestion.objects.order_by('display_order')
        context['practice_questions'] = base_qs.filter(is_test_question=True)
        questions = base_qs.filter(is_test_question=False)
        context['questions'] = self.split_list(questions, 20)
        return context


class MultipleChoiceExperimentView(generic.TemplateView):
    template_name = 'experiments/multiple_choice.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_qs = MultipleChoiceQuestion.objects.order_by('order').prefetch_related(
            Prefetch('stimuli', to_attr='stimuli_list'))
        context['practice_questions'] = base_qs.filter(is_test_question=True)
        context['questions'] = base_qs.filter(is_test_question=False)
        return context


class SingleChoiceResultView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = SingleChoiceResult.objects.all()
    serializer_class = SingleChoiceResultSerializer


class MultipleChoiceResultView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = MultipleChoiceResult.objects.all()
    serializer_class = MultipleChoiceResultSerializer
