import os

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from analytics.models import Report
from analytics.serializers import ReportSerializer
from analytics.tasks import handle_report


class ReportViewSet(ModelViewSet):
    """"""

    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    http_method_names = ['get', 'post', 'head', 'delete', 'options']
    
    def destroy(self, request, *args, **kwargs):
        report = self.get_object()
        if os.path.exists(report.file.path):
            os.remove(report.file.path)
        
        return super(ReportViewSet, self).destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def start_processing(self, request, pk=None):
        """Starts processing of the report"""
        report = self.get_object()

        if not report:
            return Response(
                {'detail': "Report with id={} not found.".format(pk)}, status=status.HTTP_404_NOT_FOUND)

        report.status = Report.IN_PROGRESS
        report.save()

        handle_report.delay(pk)

        return Response(status=status.HTTP_200_OK)
