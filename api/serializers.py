from orders_app.models import Category, Item, Customer, Order
from rest_framework import serializers


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'price', 'category', 'unit']


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name']


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'status']
