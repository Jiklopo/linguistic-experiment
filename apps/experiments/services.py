import csv
from io import StringIO
from itertools import groupby

from django.core.files.base import ContentFile
from django.db.models import Count, Q, FilteredRelation, F, Avg, Value, CharField
from django.db.models.functions import Substr, Concat, Cast
from django.utils import timezone

from apps.experiments.single_choice_models import SingleChoiceExport, SingleChoiceQuestion
from apps.experiments.utils import extract_file_name

GROUP_NAMES = ('A', 'B', 'C')


def export_single_choice_results(results_qs):
    results_qs = results_qs.annotate(group_name=Substr('notes', 1, 1))
    results_qs = results_qs.filter(group_name__in=GROUP_NAMES).order_by('group_name')
    result_groups = groupby(results_qs.values('group_name', 'id'), key=lambda x: x['group_name'])
    grouped_result_ids = {group: [item['id'] for item in group_data] for group, group_data in result_groups}

    questions = SingleChoiceQuestion.objects.order_by('order')
    for group_name in GROUP_NAMES:
        results_ids = grouped_result_ids.get(group_name, [])
        answers_field = f'answers_{group_name}'
        questions = questions.annotate(**{
            answers_field: FilteredRelation(
                'answers', condition=Q(
                    answers__result_id__in=results_ids
                )
            ),
            f'total_answers_{group_name}': Count(answers_field),
            f'correct_answers_{group_name}': Count(answers_field, filter=Q(**{f'{answers_field}__is_correct':True})),
            f'correct_percentage_{group_name}': 1.0 * F(f'correct_answers_{group_name}') / F(f'total_answers_{group_name}'),
            f'average_response_time_{group_name}': Avg(f'answers_{group_name}__response_time_ms')
        })

    with StringIO() as string_buffer:
        csv_writer = csv.writer(string_buffer)
        annotate_single_choice_results(csv_writer)
        for q in questions:
            add_single_choice_result_to_csv(csv_writer, q)

        content_file = ContentFile(string_buffer.getvalue())

    export = SingleChoiceExport()
    now = timezone.now().astimezone()
    export.export_file.save(now.strftime('%d.%m.%Y__%H-%M-%S.csv'), content_file, save=True)
    return export


def annotate_single_choice_results(csv_writer):
    group_names = ('', '', '', '', 'A', '', 'B', '', 'C', '')
    column_names = ('Question number', 'Sample 1', 'Sample 2', 'Stimulus',
                    '% correct response', 'Average response time ms',
                    '% correct response', 'Average response time ms',
                    '% correct response', 'Average response time ms')
    csv_writer.writerow(group_names)
    csv_writer.writerow(column_names)


def add_single_choice_result_to_csv(csv_writer, question):
    row = [
        question.order,
        extract_file_name(question.first_sample),
        extract_file_name(question.second_sample),
        extract_file_name(question.stimulus)
    ]
    for group_name in GROUP_NAMES:
        row.append(round(getattr(question, f'correct_percentage_{group_name}'), 3))
        row.append(round(getattr(question, f'average_response_time_{group_name}')))

    csv_writer.writerow(row)
