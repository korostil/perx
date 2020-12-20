from datetime import datetime
from typing import Generator, List
from zipfile import BadZipFile

from django.db import models
from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException
from rest_framework.exceptions import ValidationError


def validate_xls_file(file_path: str) -> None:
    """Excel file validation"""

    try:
        load_workbook(filename=file_path)
    except (InvalidFileException, BadZipFile):
        raise ValidationError(
            "Incorrect type of file! Please, upload valid excel file."
        )


class Report(models.Model):
    """Stores report file, the status of processing and result"""

    UPLOADED = 1
    IN_PROGRESS = 2
    DONE = 3

    STATUS_CHOICES = (
        (UPLOADED, "Uploaded"),
        (IN_PROGRESS, "In progress"),
        (DONE, "Done"),
    )

    uploaded = models.DateTimeField(auto_now_add=True)
    processing_finished = models.DateTimeField(null=True, blank=True)
    file = models.FileField(validators=[validate_xls_file])
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=UPLOADED)
    result = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Report, self).save(*args, **kwargs)

    def finish_processing(self, result: str) -> None:
        self.result = result
        self.processing_finished = datetime.now()
        self.status = self.DONE
        self.save(update_fields=["result", "processing_finished", "status"])

    @classmethod
    def find_diff(cls, before: Generator, after: List[int]) -> str:
        """Finds a positive number that was removed or added, or returns None if before and after are identical

        Args:
            before: generator of positive values from column "before"
            after: list of positive values in column "after"

        Returns:
            the result of adding or removing one positive number or None
        """

        after_copy = after[:]

        for item in before:
            if not after_copy:
                return "removed: {}".format(item)

            try:
                after_copy.remove(item)
            except ValueError:
                return "removed: {}".format(item)

        return "added: {}".format(after_copy[0]) if after_copy else None
