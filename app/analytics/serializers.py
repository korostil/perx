from analytics.models import Report
from rest_framework import serializers


class ReportSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = Report
        fields = ("id", "uploaded", "processing_finished", "status", "result", "file")
        read_only_fields = ("id", "uploaded", "processing_finished", "status", "result")
