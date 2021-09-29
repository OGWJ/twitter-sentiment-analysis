import pytest
from middleware import QueryChecker


app = None
query_checker = QueryChecker(app)


test_cases = [('test', True),
              # must be 0 < len < 501
              ('a'*501, False),
              ('', False),
              # cannot use invalid characters
              ('^', False),
              ('*', False),
              # cannot have leading spaces
              (' test', False),
              # cannot have trailing spaces
              ('test ', False),
              # cannot have double spaces
              ('a  b', False)]


@pytest.mark.parametrize('query, expected', test_cases)
def test_query_checker_is_valid_query(query, expected):
    assert query_checker.is_valid_query(query) == expected
