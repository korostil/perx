from datetime import datetime
from itertools import takewhile

from celery import shared_task
from openpyxl import load_workbook


@shared_task
def handle_report(report_id: int) -> None:
    """"""

    from analytics.models import Report
    report = Report.objects.get(pk=report_id)
    workbook = load_workbook(report.file)
    x = None

    for sheet_name in workbook.sheetnames:
        sheet = workbook[sheet_name]
        after_idx = before_idx = ''
        for idx, (value,) in enumerate(sheet.iter_cols(min_row=1, max_row=1, values_only=True), start=1):
            if value == 'after':
                after_idx = idx
            elif value == 'before':
                before_idx = idx

            if after_idx and before_idx:
                after_values = [
                    value
                    for (value,) in takewhile(
                        lambda x: x is not None,
                        sheet.iter_rows(min_row=2, min_col=after_idx, max_col=after_idx, values_only=True)
                    )
                    if value
                ]
                for (value,) in sheet.iter_rows(min_row=2, min_col=before_idx, max_col=before_idx, values_only=True):
                    if not after_values:
                        x = 'removed: {}'.format(value)
                    else:
                        try:
                            after_values.remove(value)
                        except ValueError:
                            x = 'added: {}'.format(after_values[0])
                break

    report.result = x
    report.processing_finished = datetime.now()
    report.status = Report.DONE
    report.save(update_fields=['result', 'processing_finished', 'status'])
