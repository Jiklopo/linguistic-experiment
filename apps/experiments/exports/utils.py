from itertools import groupby

from django.core.files.base import ContentFile
from django.db.models.functions import Substr
from django.utils import timezone

from apps.experiments.exports import GROUP_NAMES


def extract_file_name(file):
    file_name = file.name.split('/')[-1]
    no_extension = file_name.split('.')[0]
    no_label = no_extension.split('_')[0]
    return no_label


def group_results_by_group_name(results_qs):
    results_qs = results_qs.annotate(group_name=Substr('notes', 1, 1))
    results_qs = results_qs.filter(group_name__in=GROUP_NAMES).order_by('group_name')
    result_groups = groupby(results_qs.values('group_name', 'id'), key=lambda x: x['group_name'])
    grouped_result_ids = {group: [item['id'] for item in group_data] for group, group_data in result_groups}
    return grouped_result_ids


def create_export(string_buffer, export_model):
    content_file = ContentFile(string_buffer.getvalue())
    export = export_model()
    now = timezone.now().astimezone()
    export.export_file.save(now.strftime('%d.%m.%Y__%H-%M-%S.csv'), content_file, save=True)
    return export
