import os

import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status

from analytics.tasks import handle_report


@pytest.mark.parametrize(
    'test_file,status_code',
    (
            (settings.BASE_DIR + '/analytics/tests/test_data/test_removed.xlsx', status.HTTP_201_CREATED),
            (settings.BASE_DIR + '/analytics/tests/test_data/test_added.xlsx', status.HTTP_201_CREATED),
            (settings.BASE_DIR + '/analytics/tests/test_data/test_empty.xlsx', status.HTTP_201_CREATED),
            (settings.BASE_DIR + '/analytics/tests/test_data/test_bad.txt', status.HTTP_400_BAD_REQUEST),
    )
)
def test_report_uploading(db, api_client, test_file, status_code):
    response = api_client.post(
        reverse('report-list'), data={'file': open(test_file, 'rb')}
    )

    assert response.status_code == status_code
    assert os.path.exists(test_file) is True


def test_report_list_retrieving(api_client, report_factory):
    report_factory(file='test_removed.xlsx')

    response = api_client.get(reverse('report-list'))

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all([field in data[0] for field in ('id', 'uploaded', 'processing_finished', 'status', 'result')])


def test_report_retrieving(api_client, report_factory):
    report = report_factory(file='test_removed.xlsx')

    response = api_client.get(reverse('report-detail', kwargs={'pk': report.id}))

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all([field in data for field in ('id', 'uploaded', 'processing_finished', 'status', 'result')])


@pytest.mark.parametrize(
    'test_file,expected',
    [
        ('test_removed.xlsx', 'removed: 6'),
        ('test_added.xlsx', 'added: 78'),
        ('test_empty.xlsx', None),
    ]
)
def test_report_handling(report_factory, test_file, expected):
    report = report_factory(file=test_file)

    handle_report(report.id)
    report.refresh_from_db()
    
    assert report.result == expected


def test_non_exists_report_handling(api_client, report_factory):
    report = report_factory(file='test_removed.xlsx')

    response = api_client.get(reverse('report-detail', kwargs={'pk': report.id + 10000}))

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    'test_file', ('test_removed.xlsx', 'test_added.xlsx', 'test_empty.xlsx',)
)
def test_report_deleting(api_client, report_factory, test_file):
    report = report_factory(file=test_file)

    response = api_client.delete(reverse('report-detail', kwargs={'pk': report.id}))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert os.path.exists(report.file.path) is False
