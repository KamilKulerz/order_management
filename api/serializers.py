from orders_app.models import Category, Item, Customer, Order, OrderedItem
from rest_framework import serializers


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'price', 'category', 'unit')


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'name')


class OrderedItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderedItem
        fields = ('id', 'item', 'quantity', 'status')


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    items = OrderedItemSerializer(source='ordereditem_set', many=True)

    class Meta:
        model = Order
        fields = ('id', 'customer', 'status', 'items')
