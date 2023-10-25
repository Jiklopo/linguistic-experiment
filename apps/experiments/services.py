import csv
from io import StringIO

from django.core.files.base import ContentFile
from django.utils import timezone

from apps.experiments.choices import CorrectSampleChoices
from apps.experiments.single_choice_models import SingleChoiceResult, SingleChoiceExport


def extract_file_name(file):
    file_name = file.name.split('/')[-1]
    no_extension = file_name.split('.')[0]
    no_label = no_extension.split('_')[0]
    return no_label


def export_single_choice_results(results_qs):
    with StringIO() as string_buffer:
        csv_writer = csv.writer(string_buffer)
        results_qs = results_qs.prefetch_related('answers__question')
        for index, result in enumerate(results_qs):
            add_single_choice_result_to_csv(csv_writer, result, index == 0)

        content_file = ContentFile(string_buffer.getvalue())

    export = SingleChoiceExport()
    now = timezone.now().astimezone()
    export.export_file.save(now.strftime('%d.%m.%Y__%H-%M-%S.csv'), content_file, save=True)
    return export


def add_single_choice_result_to_csv(csv_writer, result: SingleChoiceResult, add_labels=False):
    if add_labels:
        column_names = ('Sample 1', 'Sample 2', 'Stimulus', 'Correct sample',
                        'Selected sample', 'Is correct', 'Response time ms')
        csv_writer.writerow(column_names)

    for answer in result.answers.all():
        csv_writer.writerow((
            extract_file_name(answer.question.first_sample),
            extract_file_name(answer.question.second_sample),
            extract_file_name(answer.question.stimulus),
            CorrectSampleChoices.to_number(answer.question.correct_sample),
            CorrectSampleChoices.to_number(answer.selected_sample),
            int(answer.is_correct),
            answer.response_time_ms
        ))
