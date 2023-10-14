from django.views import generic
from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.experiments.models import SingleChoiceQuestion, SingleChoiceResult
from apps.experiments.serializers import SingleChoiceResultSerializer


class SingleChoiceExperimentView(generic.TemplateView):
    template_name = 'experiments/single_choice.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = SingleChoiceQuestion.objects.all()
        return context


class SingleChoiceResultView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = SingleChoiceResult.objects.all()
    serializer_class = SingleChoiceResultSerializer
