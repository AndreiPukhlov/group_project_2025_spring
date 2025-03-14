from pprint import pprint

import pytest

from database.film2_queries.film_queries import get_all_data, count_all_rows, get_movies_1940_1970, \
    movies_where_writer_is


def test_get_all_data():
    result = get_all_data()
    pprint(result)


def test_count_all_rows():
    result = count_all_rows()
    actual_result = result[0]
    assert actual_result == 1976


def test_get_movies_1940_1970():
    result = get_movies_1940_1970()
    for i in result:
        assert 1940 <= i[4] <= 1970


@pytest.mark.parametrize("writer", ['Eric von Stroheim', 'Kathryn Scola', 'Joe Eszterhas',
                                    'Lana Wachowski, David Mitchell, Aleksander Hemon'])
def test_movies_where_writer_is(writer):
    result = movies_where_writer_is(writer)
    for i in result:
        assert i[3] == writer
