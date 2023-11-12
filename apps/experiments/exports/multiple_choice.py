import csv
from io import StringIO
from itertools import groupby

from django.db.models import Count, Q, FilteredRelation, F, Avg

from apps.experiments.choices import CorrectSampleChoices
from apps.experiments.exports import GROUP_NAMES
from apps.experiments.exports.utils import group_results_by_group_name, create_export
from apps.experiments.multiple_choice_models import Stimulus, MultipleChoiceExport


def export_multiple_choice_results(results_qs):
    grouped_result_ids = group_results_by_group_name(results_qs)
    stimuli = Stimulus.objects.order_by('question__order', 'order')

    for group_name in GROUP_NAMES:
        results_ids = grouped_result_ids.get(group_name, [])
        answers_field = f'answers_{group_name}'
        stimuli = stimuli.annotate(**{
            answers_field: FilteredRelation('answers', condition=Q(answers__result_id__in=results_ids)),
            f'total_answers_{group_name}': Count(answers_field),
            f'first_answers_{group_name}': Count(answers_field, filter=Q(
                **{f'{answers_field}__selected_sample': CorrectSampleChoices.FIRST})),
            f'first_percentage_{group_name}': 1.0 * F(f'first_answers_{group_name}') / F(f'total_answers_{group_name}'),
            f'average_response_time_{group_name}': Avg(f'answers_{group_name}__response_time_ms')
        })

    grouped_stimuli = groupby(stimuli, key=lambda x: x.question.order)
    with StringIO() as string_buffer:
        csv_writer = csv.writer(string_buffer)
        for question_order, stimuli_data in grouped_stimuli:
            annotate_results(csv_writer, question_order)
            for s in stimuli_data:
                add_results_to_csv(csv_writer, s)
            csv_writer.writerow(('', '', '', '', '', '', ''))
            csv_writer.writerow(('', '', '', '', '', '', ''))

        return create_export(string_buffer, MultipleChoiceExport)


def annotate_results(csv_writer, question_number):
    question_row = ('', '', '', f'Q{question_number}', '', '', '')
    group_names = ('', 'A', '', 'B', '', 'C', '')
    column_names = ('Stimulus',
                    '% "First" response', 'Average response time ms',
                    '% "First" response', 'Average response time ms',
                    '% "First" response', 'Average response time ms')
    csv_writer.writerow(question_row)
    csv_writer.writerow(group_names)
    csv_writer.writerow(column_names)


def add_results_to_csv(csv_writer, stimulus):
    row = [stimulus.order]
    for group_name in GROUP_NAMES:
        row.append(round(getattr(stimulus, f'first_percentage_{group_name}'), 3))
        row.append(round(getattr(stimulus, f'average_response_time_{group_name}')))

    csv_writer.writerow(row)
