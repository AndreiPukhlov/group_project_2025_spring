from pprint import pprint

import requests

BASE_ENDPOINT = "https://simple-grocery-api.store/"
STATUS = "status/"
PRODUCTS = "products/"
CARTS = "carts/"
ITEMS = 'items/'
AUTHORIZATION = 'api-clients/'


def test_status():
    response = requests.get(BASE_ENDPOINT + STATUS)
    assert response.json()['status'] == "UP"
    assert response.status_code == 200


def test_all_products():
    response = requests.get(BASE_ENDPOINT + PRODUCTS)
    pprint(response.json(), indent=4)
    assert len(response.json()) == 20
    assert len(str(response.json()[0]['id'])) == 4


def test_add_cart():
    response = requests.post(BASE_ENDPOINT + CARTS)
    print(response.json())
    print(response.json()['cartId'])
    assert response.json()['created']
    assert response.status_code == 201


def test_token():
    json = {
        "clientName": "User",
        "clientEmail": "user@mail.com"
    }
    response = requests.post(BASE_ENDPOINT + AUTHORIZATION, json=json)
    print(response.json())
