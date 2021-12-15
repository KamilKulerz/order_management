from django.shortcuts import render

# Create your views here.
from orders_app.models import Category, Item, Order, Customer
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from .serializers import CategorySerializer, CustomerSerializer, OrderSerializer, ItemSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('name')
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('name')
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('customer')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
