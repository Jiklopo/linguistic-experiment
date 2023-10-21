from django.views import generic
from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.experiments.single_choice_models import SingleChoiceQuestion, SingleChoiceResult
from apps.experiments.serializers import SingleChoiceResultSerializer


class SingleChoiceExperimentView(generic.TemplateView):
    template_name = 'experiments/single_choice.html'

    @staticmethod
    def split_list(input_list, chunk_size):
        return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_qs = SingleChoiceQuestion.objects.order_by('order')
        context['practice_questions'] = base_qs.filter(is_test_question=True)
        questions = base_qs.filter(is_test_question=False)
        context['questions'] = self.split_list(questions, 3)
        return context


class SingleChoiceResultView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = SingleChoiceResult.objects.all()
    serializer_class = SingleChoiceResultSerializer
