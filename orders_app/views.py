from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.urls.base import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import DeleteView
from orders_app.models import Order, Item, Customer, Category, OrderedItem
from django.urls import reverse, resolve
from django.core import serializers


def index(request):

    html = "<html><body>It is now </body></html>"
    return HttpResponse(html)


def home(request):
    context = {}
    return render(request, 'orders_app/home.html', context)


# class OrdersList(ListView):
#     model = Order
#     template_name = 'orders_app/order_list.html'

def order_list(request):

    context = {}

    if request.method == 'GET':
        queryset = Order.objects.all()
        context['object_list'] = queryset
    return render(request, 'orders_app/order_list.html', context)


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('orders_app:orders')


class OrderDetail(DetailView):
    model = Order
    # context_object_name = "issue"
    template_name = "orders_app/order_detail.html"


class OrderedItemDetail(DetailView):
    model = OrderedItem
    # context_object_name = "issue"
    template_name = "orders_app/ordereditem_detail.html"


class ItemsList(ListView):
    model = Item
    template_name = 'orders_app/item_list.html'


class CustomersList(ListView):
    model = Customer
    template_name = 'orders_app/customer_list.html'


class CategoriesList(ListView):
    model = Category
    template_name = 'orders_app/category_list.html'


class ItemCreateView(CreateView):
    model = Item
    fields = ['name', 'price', 'category_id', 'unit']

    def get_success_url(self):  # new
        return reverse('orders_app:items')


class OrderCreateView(CreateView):
    model = Order
    fields = ['customer_id', 'status']

    def get_success_url(self):  # new
        return reverse('orders_app:orders')


class OrderedItemCreateView(CreateView):
    model = OrderedItem
    fields = ['item', 'quantity', 'status']

    def get_success_url(self):  # new
        # return resolve(f'/orders/{self.request.GET["order_id"]}')
        return reverse('orders_app:orders')

    def form_valid(self, form):
        #!!!!!!!!!!!!!!!!!!!!!!!
        form.instance.order_id = Order.objects.get(
            id=self.request.GET['order_id'])
        return super(OrderedItemCreateView, self).form_valid(form)


class CustomerCreateView(CreateView):
    model = Customer
    fields = ['name']

    def get_success_url(self):  # new
        return reverse('orders_app:customers')
