from pprint import pprint

from database.film2_queries.film_queries import get_all_data, count_all_rows


def test_get_all_data():
    result = get_all_data()
    pprint(result)


def test_count_all_rows():
    result = count_all_rows()
    actual_result = result[0]
    assert actual_result == 1976
