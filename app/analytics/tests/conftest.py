import pytest

from mixer.backend.django import mixer


@pytest.fixture
def report_factory(db):
    def _report(**kwargs):
        return mixer.blend('analytics.Report', **kwargs)

    return _report
