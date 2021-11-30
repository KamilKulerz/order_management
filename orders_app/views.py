from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import DeleteView
from orders_app.models import Order, Item, Customer, Category, OrderedItem, ORDER_STATUSES
from django.urls import reverse, resolve
from django.core import serializers
from django.forms import inlineformset_factory
from django.contrib import messages
from .forms import OrderForm
from django.db.models import Count


def index(request):

    html = "<html><body>It is now </body></html>"
    return HttpResponse(html)


def home(request):
    STATUS_COL_NAME = 'status'
    context = {}
    no_of_orders = Order.objects.all().count()
    groupped = (Order.objects
                .values(STATUS_COL_NAME)
                .annotate(Count(STATUS_COL_NAME))
                .order_by()
                )

    order_statuses_reverse = dict((k, v) for k, v in ORDER_STATUSES)
    for x in groupped:
        x[STATUS_COL_NAME] = order_statuses_reverse[x[STATUS_COL_NAME]]

    # groupped = [{STATUS_COL_NAME: order_statuses_reverse[x[STATUS_COL_NAME]],
    #              'status__count': x['status__count']} for x in groupped]

    print(groupped)
    context['no_of_orders'] = no_of_orders
    context['groupped_summary'] = groupped
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


# class OrderDetail(DetailView):
#     model = Order
#     # context_object_name = "issue"
#     template_name = "orders_app/order_detail.html"

def order_detail_update(request, pk):
    if request.method == 'POST':
        queryset = Order.objects.get(id=pk)
        OrderFormSet = inlineformset_factory(
            Order, OrderedItem, fields=('status', 'quantity'), extra=0)
        formset = OrderFormSet(request.POST, request.FILES, instance=queryset)
        if formset.is_valid():
            formset.save()
            messages.info(request, 'Order saved succesfully!')
        else:
            # TODO add wrond form handling
            print(formset.errors)
        return HttpResponseRedirect(reverse('orders_app:order', kwargs={'pk': pk}))


def order_update(request, pk):
    queryset = Order.objects.get(id=pk)
    if request.method == 'POST':
        order_form = OrderForm(request.POST, request.FILES, instance=queryset)
        if order_form.is_valid():
            order_form.save()
            messages.info(request, 'Order updated!')
        else:
            print(order_form.errors)
        return HttpResponseRedirect(reverse('orders_app:order', kwargs={'pk': pk}))


def order_detail(request, pk):
    context = {}

    if request.method == 'GET':

        queryset = Order.objects.get(id=pk)
        OrderFormSet = inlineformset_factory(
            Order, OrderedItem, fields=('status', 'quantity'), extra=0)
        order_form = OrderForm(instance=queryset)
        formset = OrderFormSet(instance=queryset)

        context['order'] = queryset
        context['formset'] = formset
        context['order_form'] = order_form
        context['queryset_formset'] = zip(
            list(queryset.ordereditem_set.all()), list(formset))
    return render(request, 'orders_app/order_detail.html', context)


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
        return reverse('orders_app:order', kwargs={'pk': self.request.GET["order_id"]})

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


class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']

    def get_success_url(self):  # new
        return reverse('orders_app:categories')
