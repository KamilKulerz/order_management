import pytest
from api.views import CategoryViewSet
from django.urls import reverse
from orders_app.models import Category
from rest_framework import response, status
from rest_framework.test import APIClient, APIRequestFactory


def test_api_root_get(new_client, new_user):

    new_client.login(username=new_user.username, password=new_user.password)
    url = f'/api/'
    response = new_client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_categories_get(new_client, new_cat, new_user):

    new_client.force_authenticate(user=new_user)
    url = f'/api/categories/'
    response = new_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


def test_categories_single_get(new_client, new_cat, new_user):

    new_client.force_authenticate(user=new_user)
    url = f'/api/categories/{new_cat.id}/'
    response = new_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == new_cat.name


def test_categories_single_post(new_client, new_user):

    new_client.force_authenticate(user=new_user)
    url = f'/api/categories/'
    data = {'name': 'test cat 99'}
    response = new_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Category.objects.filter(name=data['name']).exists()


# def test_categories_single_put(new_cat, new_user):

#     client = APIClient()
#     client.force_authenticate(user=new_user)
#     url = f'/api/categories/{new_cat.id}'
#     data = {'name': 'test cat 99'}
#     response = client.put(url, data, format='json')
#     assert response.status_code == status.HTTP_200_OK
#     assert Category.objects.get(id=new_cat.id).name == data['name']
