from zipfile import BadZipFile

from django.db import models
from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException
from rest_framework.exceptions import ValidationError


def validate_xls_file(file) -> None:
    """Excel file validation"""

    try:
        load_workbook(filename=file)
    except (InvalidFileException, BadZipFile):
        raise ValidationError('Incorrect type of file! Please, upload valid excel file.')


class Report(models.Model):
    """Stores report file, the status of processing and result"""

    UPLOADED = 1
    IN_PROGRESS = 2
    DONE = 3

    STATUS_CHOICES = (
        (UPLOADED, 'Uploaded'),
        (IN_PROGRESS, 'In progress'),
        (DONE, 'Done')
    )

    uploaded = models.DateTimeField(auto_now_add=True)
    processing_finished = models.DateTimeField(null=True, blank=True)
    file = models.FileField(validators=[validate_xls_file])
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=UPLOADED)
    result = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Report, self).save(*args, **kwargs)
