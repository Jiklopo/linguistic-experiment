from django.core.management import BaseCommand

from apps.experiments.single_choice_models import SingleChoiceQuestion


class Command(BaseCommand):
    def handle(self, *args, **options):
        questions = SingleChoiceQuestion.objects.order_by('?')
        for i, question in enumerate(questions):
            question.display_order = i
            question.save()