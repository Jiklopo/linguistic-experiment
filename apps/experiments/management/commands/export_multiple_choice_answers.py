import csv
import os
from uuid import uuid4

from django.core.management import BaseCommand

from apps.experiments.choices import CorrectSampleChoices
from apps.experiments.exports.utils import extract_file_name
from apps.experiments.multiple_choice_models import MultipleChoiceAnswer


class Command(BaseCommand):
    @staticmethod
    def get_file_name(file):
        return file.name.split('/')[-1]

    def handle(self, *args, **options):
        answers = MultipleChoiceAnswer.objects.order_by('result__notes', 'stimulus__question__order', 'stimulus__order')
        answers = answers.select_related('stimulus__question', 'result')
        directory = 'media/exports/answers'
        filename = f'{directory}/{uuid4()}.csv'
        os.makedirs(directory, exist_ok=True)

        with open(filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(('Subject', 'Question number', 'Stimulus number', 'Selected sample', 'Response time ms',
                             'Date', 'First sample',
                             'Second sample', 'Stimulus'))
            for answer in answers:
                writer.writerow((
                    answer.result.notes,
                    answer.stimulus.question.order,
                    answer.stimulus.order,
                    CorrectSampleChoices.to_number(answer.selected_sample),
                    answer.response_time_ms,
                    answer.result.created_at.strftime('%d.%m.%Y %H:%M %Z'),
                    extract_file_name(answer.stimulus.question.first_sample),
                    extract_file_name(answer.stimulus.question.second_sample),
                    extract_file_name(answer.stimulus.file)
                ))

        return filename
