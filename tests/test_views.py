import pytest
from django.test.client import Client
from orders_app.models import Order
from rest_framework import status


def test_home_view(new_client, new_order):

    url = f'/'
    response = new_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.context['no_of_orders'] == 1
    assert len(response.context['groupped_summary']) == 1


def test_order_detail_view(new_client, new_cat, new_order, new_item_factory, ordereditem_factory):
    it1 = new_item_factory('test1', 15.5, new_cat, 'szt.')
    it2 = new_item_factory('test2', 15.5, new_cat, 'szt.')
    ordereditem_factory(it1, 10, new_order, Order.ORDER_STATUSES[0][0])
    ordereditem_factory(it2, 10, new_order, Order.ORDER_STATUSES[0][0])

    url = f'/orders/{new_order.id}'
    response = new_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.context['order'].id == 1
    assert len(list(response.context['formset'])) == 2
    assert 'status' in response.context['order_form'].fields.keys()
    assert response.context['summary_data'] == [{'status': 'nok', 'status__count': 2}]


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
