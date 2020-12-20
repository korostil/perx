import pytest
from analytics.models import Report


@pytest.mark.parametrize(
    "before,after,expected",
    (
        ([1, 1, 1, 1, 1], [2, 1, 1, 1, 1, 1], "added: 2"),
        ([1, 1, 1, 1, 1], [1, 2, 1, 1, 1, 1], "added: 2"),
        ([1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 2], "added: 2"),
        ([2, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1], "removed: 2"),
        ([], [], None),
        ([1], [1], None),
        ([1], [], "removed: 1"),
        ([], [1], "added: 1"),
    ),
)
def test_diff_calculation(before, after, expected):
    assert Report.find_diff((_ for _ in before), after) == expected
