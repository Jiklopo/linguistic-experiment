import csv
import os
from uuid import uuid4

from django.core.management import BaseCommand

from apps.experiments.exports.utils import extract_file_name
from apps.experiments.single_choice_models import SingleChoiceAnswer


class Command(BaseCommand):
    @staticmethod
    def get_file_name(file):
        return file.name.split('/')[-1]

    def handle(self, *args, **options):
        answers = SingleChoiceAnswer.objects.order_by('result__notes', 'question__order')
        answers = answers.select_related('question', 'result')
        directory = 'media/exports/answers'
        filename = f'{directory}/{uuid4()}.csv'
        os.makedirs(directory, exist_ok=True)

        with open(filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(('Subject', 'Question number', 'Is correct', 'Response time ms', 'Date', 'First sample',
                             'Second sample', 'Stimulus'))
            for answer in answers:
                writer.writerow((
                    answer.result.notes,
                    answer.question.order,
                    int(answer.is_correct),
                    answer.response_time_ms,
                    answer.result.created_at.strftime('%d.%m.%Y %H:%M %Z'),
                    extract_file_name(answer.question.first_sample),
                    extract_file_name(answer.question.second_sample),
                    extract_file_name(answer.question.stimulus)
                ))

        return filename
