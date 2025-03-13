
from decimal import Decimal
from pprint import pprint

import pytest

from database.classic_model_quires.classic_models_queries import *


def test_get_top_vendor():
    """Test the get_top_vendor function using a fixture."""
    result = get_top_vendor()
    print(result)
    assert result is not None


@pytest.mark.parametrize("country", ["USA", "France", "Germany"])
def test_fetch_customers_by_country(db_connection, country):
    result = fetch_customers_by_country(country)
    pprint(result, indent=4)

    def func():
        for i in result:
            if i.__contains__(country):
                return True
            else:
                return False
    assert func()


def test_get_vendors_product_lines_products():
    result = get_vendors_product_lines_products()
    print(result)
    assert result == (110, 7, 13)


def test_get_avg_msrp_buy_price():
    result = get_avg_msrp_buy_price()
    pprint(result, indent=4)
    print(f"Result returned {len(result)} rows")
    assert result.__contains__(('Second Gear Diecast', Decimal('59.687500'), Decimal('113.503750')))
    assert len(result) == 13


def test_number_of_vendors_product_lines_products():
    result = number_of_vendors_product_lines_products()
    print(result)
    return result is not None


def test_max_sails_vendor():
    result = max_sails_vendor()
    print(result)
    from decimal import Decimal
    assert result == ('Classic Metal Creations', Decimal('9678'))


def test_most_sold_product():
    result = most_sold_product()
    print(result)
    assert result == ('1992 Ferrari 360 Spider red', Decimal('1808'))


def test_buyprice_msrp_difference():
    result = buyprice_msrp_difference()
    pprint(result, indent=4)
    assert result[0] == ('18th century schooner',
                         Decimal('82.34'),
                         Decimal('122.89'),
                         Decimal('-40.55'))


def test_get_union_buy_price():
    result = get_union_buyprice()
    assert len(result) == 110


def test_get_all_canceled_orders():
    respond = get_all_canceled_orders()
    assert respond[0] == 6


def test_all_orders_created():
    result = all_orders_created()
    assert result[0] == 326


def test_number_of_products_per_product_line():
    expected_list = [('Classic Cars', 38), ('Motorcycles', 13), ('Planes', 12), ('Ships', 9), ('Trains', 3),
                     ('Trucks and Buses', 11), ('Vintage Cars', 24)]
    result = number_of_products_per_product_line()
    assert result == expected_list


def test_number_of_no_customer_employees():
    result = number_of_no_customer_employees()
    assert result[0] == 8
