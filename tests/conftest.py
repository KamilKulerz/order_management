import decimal

import pytest
from django.contrib.auth.models import User
from orders_app.models import Category, Customer, Item, Order, OrderedItem
from rest_framework.test import APIClient


@pytest.fixture()
def new_client():
    client = APIClient()
    return client


@pytest.fixture()
def user_1(db):
    return User.objects.create_user('test', 'test@test.com', 'test')


@pytest.fixture()
def new_customer(db):
    cust = Customer.objects.create(name='test')
    return cust


@pytest.fixture()
def new_cat(db):
    cat = Category.objects.create(name='test cat')
    return cat


@pytest.fixture()
def ordereditem_factory(db):
    def create_ordereditem(item: Item, quantity: int, order: Order, status: str):
        ordereditem = OrderedItem.objects.create(
            item=item,
            quantity=quantity,
            order=order,
            status=status
        )
        return ordereditem
    return create_ordereditem


@pytest.fixture()
def new_item_factory(db):
    def create_item(name: str, price: float, category: Category, unit: str):
        item = Item.objects.create(
            name=name,
            price=price,
            category=category,
            unit=unit
        )
        return item
    return create_item


@pytest.fixture()
def new_item(db, new_item_factory, new_cat):
    return new_item_factory('test item', 10.01, new_cat, 'szt.')


@pytest.fixture()
def new_user_factory(db):
    def create_app_user(
        username: str,
        password: str = None,
        first_name: str = 'firstname',
        last_name: str = 'lastname',
        email: str = 'test@test.com',
        is_staff: bool = False,
        is_superuser: bool = False,
        is_active: bool = True,
    ):
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
        )
        return user
    return create_app_user


@pytest.fixture()
def new_order_factory(db):
    def create_order(customer: Customer, status: str):
        order = Order.objects.create(
            customer=customer,
            status=status,
        )
        return order
    return create_order


@pytest.fixture()
def new_user(db, new_user_factory):
    return new_user_factory('test user', 'pass', 'name')


@pytest.fixture()
def new_order(db, new_order_factory, new_customer):
    return new_order_factory(new_customer, 'nok')
