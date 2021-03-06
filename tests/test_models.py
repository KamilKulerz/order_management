from django.db import IntegrityError
import pytest
from django.contrib.auth.models import User
from orders_app.models import Category, Customer, Item, Order, OrderedItem


@pytest.mark.django_db
def test_user_create(user_1):
    assert User.objects.count() == 1


def test_customer_str(new_customer):
    assert str(new_customer) == 'test'


def test_order_str(new_order):
    assert str(new_order) == '1'


def test_item_str(new_item):
    assert str(new_item) == 'test item'


def test_category_str(new_cat):
    assert str(new_cat) == 'test cat'


def test_new_user(new_user):
    assert new_user.first_name == 'name'


def test_create_customer(new_customer):
    cust_from_db = Customer.objects.get(id=new_customer.id)
    assert Customer.objects.count() == 1
    assert cust_from_db.name == new_customer.name


def test_create_category(new_cat):
    cat_from_db = Category.objects.get(id=new_cat.id)
    assert Category.objects.count() == 1
    assert cat_from_db.name == new_cat.name


def test_create_item(new_item, new_cat):
    item_from_db = Item.objects.get(id=new_item.id)
    assert Item.objects.count() == 1
    assert item_from_db.name == new_item.name
    assert item_from_db.price == new_item.price
    assert item_from_db.category == new_cat
    assert item_from_db.unit == new_item.unit


def test_create_order_empty(new_order, new_customer):
    order_from_db = Order.objects.get(id=new_order.id)
    assert Order.objects.count() == 1
    assert order_from_db.customer == new_customer
    assert order_from_db.status == new_order.status
    assert len(order_from_db.get_ordered_items()) == 0


def test_create_order_with_item(new_order, new_item):
    new_ordered_item = OrderedItem.objects.create(
        item=new_item, quantity=10, order=new_order)

    items = new_order.get_ordered_items()

    assert len(items) == 1
    assert items[0].name == new_item.name


def test_number_of_ordered_items(new_order, new_item):
    new_ordered_item = OrderedItem.objects.create(
        item=new_item, quantity=10, order=new_order)
    assert new_order.count_items() == 1


def test_counting_orders(new_order):
    assert Order.count_orders() == 1


def test_groupping_orders(new_order_factory, new_customer):

    order1 = new_order_factory(new_customer, 'nok')
    order2 = new_order_factory(new_customer, 'nok')
    order3 = new_order_factory(new_customer, 'pkd')
    groupped = Order.get_groupped_by_status()
    assert len(groupped) == 2
    assert groupped.get(status='nok')['status__count'] == 2
    assert groupped.get(status='pkd')['status__count'] == 1


def test_get_groupped_items_count(new_order, new_item_factory, new_cat, ordereditem_factory):
    item1 = new_item_factory('t1', 1, new_cat, 'szt.')
    item2 = new_item_factory('t2', 1, new_cat, 'szt.')
    item3 = new_item_factory('t3', 1, new_cat, 'szt.')

    ordereditem_factory(item1, 10, new_order, Order.ORDER_STATUSES[0][0])
    ordereditem_factory(item2, 15, new_order, Order.ORDER_STATUSES[1][0])
    ordereditem_factory(item3, 20, new_order, Order.ORDER_STATUSES[2][0])

    assert list(new_order.get_groupped_items_count()) == [{'status': 'nok', 'status__count': 1},
                                                          {'status': 'ong', 'status__count': 1},
                                                          {'status': 'pkd', 'status__count': 1}]


def test_get_groupped_items_sum(new_order, new_item_factory, new_cat, ordereditem_factory):
    item1 = new_item_factory('t1', 1, new_cat, 'szt.')
    item2 = new_item_factory('t2', 1, new_cat, 'szt.')
    item3 = new_item_factory('t3', 1, new_cat, 'szt.')

    ordereditem_factory(item1, 10, new_order, Order.ORDER_STATUSES[0][0])
    ordereditem_factory(item2, 15, new_order, Order.ORDER_STATUSES[1][0])
    ordereditem_factory(item3, 20, new_order, Order.ORDER_STATUSES[2][0])

    assert list(new_order.get_groupped_items_sum()) == [{'status': 'nok', 'quantity__sum': 10},
                                                        {'status': 'ong', 'quantity__sum': 15},
                                                        {'status': 'pkd', 'quantity__sum': 20}]


def test_item_update_url(new_item):
    assert new_item.get_update_url() == f'/items/{new_item.id}/update'


def test_item_delete_url(new_item):
    assert new_item.get_delete_url() == f'/items/{new_item.id}/delete'


def test_category_update_url(new_cat):
    assert new_cat.get_update_url() == f'/categories/{new_cat.id}/update'


def test_category_delete_url(new_cat):
    assert new_cat.get_delete_url() == f'/categories/{new_cat.id}/delete'


def test_customer_update_url(new_customer):
    assert new_customer.get_update_url() == f'/customers/{new_customer.id}/update'


def test_customer_delete_url(new_customer):
    assert new_customer.get_delete_url() == f'/customers/{new_customer.id}/delete'


def test_delete_cat_with_item_assigned(new_cat, new_item):
    new_cat.delete()
    assert new_item.category.id is None


def test_delete_customer_with_existing_orders(new_order, new_customer):
    new_customer.delete()
    assert new_order.customer.id is None


def test_price_less_than_0(new_item_factory, new_cat):
    with pytest.raises(IntegrityError):
        new_item_factory('test item', -10.01, new_cat, 'szt.')
