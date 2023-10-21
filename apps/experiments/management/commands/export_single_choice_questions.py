import csv
from uuid import uuid4

from django.core.management import BaseCommand

from apps.experiments.single_choice_models import SingleChoiceQuestion

import os
class Command(BaseCommand):
    @staticmethod
    def get_file_name(file):
        return file.name.split('/')[-1]

    def handle(self, *args, **options):
        questions = SingleChoiceQuestion.objects.all()
        directory = 'media/exports/questions'
        filename = f'{directory}/{uuid4()}.csv'
        os.makedirs(directory, exist_ok=True)
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(('Order', 'First sample', 'Second sample', 'Stimulus', 'Is test'))
            for question in questions:
                writer.writerow((
                    question.order,
                    self.get_file_name(question.first_sample),
                    self.get_file_name(question.second_sample),
                    self.get_file_name(question.stimulus),
                    '+' if question.is_test_question else '-'
                ))

        return filename
