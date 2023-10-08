from django.views import generic
from django.shortcuts import render

from apps.experiments.models import SingleChoiceQuestion


# Create your views here.
class SingleChoiceExperimentView(generic.TemplateView):
    template_name = 'experiments/single_choice.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = SingleChoiceQuestion.objects.all()
        return context
