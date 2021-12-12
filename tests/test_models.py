import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_user_create(user_1):
    assert User.objects.count() == 1


def test_customer_str(new_customer):
    assert str(new_customer) == 'test'


def test_item_str(new_item):
    assert str(new_item) == 'test item'


def test_category_str(new_cat):
    assert str(new_cat) == 'test cat'


def test_new_user(new_user):
    assert new_user.first_name == 'name'
