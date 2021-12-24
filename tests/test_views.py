import pytest
from rest_framework import status
from django.test.client import Client


def test_home_view(new_client, new_order):

    url = f'/'
    response = new_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.context['no_of_orders'] == 1
    assert len(response.context['groupped_summary']) == 1


@pytest.mark.parametrize("url", [
    ('/items/'),
    ('/items/add'),
    ('/items/1/update'),
    ('/items/1/delete'),
])
def test_items_access(client, url, new_user, new_item):
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("url", [
    ('/customers/'),
    ('/customers/add'),
    ('/customers/1/update'),
    ('/customers/1/delete'),
])
def test_customers_access(client, url, new_user, new_customer):
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("url", [
    ('/categories/'),
    ('/categories/add'),
    ('/categories/1/update'),
    ('/categories/1/delete'),
])
def test_categories_access(client, url, new_user, new_cat):
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("url", [
    ('/orders/'),
    ('/orders/add'),
    # ('/orders/1/update'),
    # ('/orders/1/update_items'),
    ('/orders/1/delete'),
])
def test_orders_access(client, url, new_user, new_order):
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
