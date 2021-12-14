import pytest
from orders_app.models import Customer, Order, Item, Category
from django.contrib.auth.models import User
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
def new_item(db):
    cat = Category.objects.create(name='test cat')
    itm = Item.objects.create(
        name='test item',
        price=10.01,
        category=cat,
        unit='szt.'
    )
    return itm


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
def new_user(db, new_user_factory):
    return new_user_factory('test user', 'pass', 'name')
