from typing import Any, Dict, Type

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.query import QuerySet
from django.db.utils import IntegrityError
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django_stubs_ext.aliases import ValuesQuerySet
from django.utils.translation import gettext as _

from orders_app.models import Category, Customer, Item, Order, OrderedItem

from .forms import OrderForm


def home(request) -> HttpResponse:
    no_of_orders: int
    groupped: ValuesQuerySet[Order, dict]
    order_statuses_reverse: dict

    context: Dict[str, Any] = {}
    STATUS_COL_NAME: str = 'status'

    no_of_orders = Order.count_orders()
    groupped = Order.get_groupped_by_status()
    order_statuses_reverse = dict((k, v) for k, v in Order.ORDER_STATUSES)
    for x in groupped:
        x[STATUS_COL_NAME] = order_statuses_reverse[x[STATUS_COL_NAME]]

    context['no_of_orders'] = no_of_orders
    context['groupped_summary'] = groupped

    return render(request, 'orders_app/home.html', context)


def order_list(request) -> HttpResponse:
    queryset: QuerySet[Order]

    context: Dict[str, Any] = {}

    if request.method == 'GET':
        queryset = Order.objects.all()
        context['object_list'] = queryset

    return render(request, 'orders_app/order_list.html', context)


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('orders_app:orders')


def order_detail_update(request, pk: str) -> HttpResponseRedirect:
    queryset: Order
    OrderFormSet: Type[BaseInlineFormSet]
    formset: BaseInlineFormSet

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


def order_update(request, pk: str):
    queryset: Order
    order_form: OrderForm

    queryset = Order.objects.get(id=pk)
    if request.method == 'POST':
        order_form = OrderForm(request.POST, request.FILES, instance=queryset)
        if order_form.is_valid():
            order_form.save()
            messages.info(request, 'Order updated!')
        else:
            print(order_form.errors)
        return HttpResponseRedirect(reverse('orders_app:order', kwargs={'pk': pk}))


def order_detail(request, pk: str) -> HttpResponse:
    context: Dict[str, Any] = {}

    if request.method == 'GET':
        order: Order
        OrderFormSet: Type[BaseInlineFormSet]
        order_form: OrderForm
        formset: BaseInlineFormSet
        groupped: ValuesQuerySet[OrderedItem, dict]

        order = Order.objects.get(id=pk)
        OrderFormSet = inlineformset_factory(
            Order, OrderedItem, fields=('status', 'quantity'), extra=0)
        order_form = OrderForm(instance=order)
        formset = OrderFormSet(instance=order)

        groupped = order.get_groupped_items_count()

        context['order'] = order
        context['formset'] = formset
        context['order_form'] = order_form
        context['queryset_formset'] = zip(list(order.ordereditem_set.all()), list(formset))
        context['summary_data'] = list(groupped)
    return render(request, 'orders_app/order_detail.html', context)


class OrderCreateView(CreateView):
    model = Order
    fields = ['customer', 'status']

    def get_success_url(self):  # new
        return reverse('orders_app:orders')


class OrderedItemDetail(DetailView):
    model = OrderedItem
    # context_object_name = "issue"
    template_name = "orders_app/ordereditem_detail.html"


class OrderedItemCreateView(CreateView):
    model = OrderedItem
    fields = ['item', 'quantity', 'status']
    # form_class = OrderedItemForOrderForm

    def post(self, request, *args, **kwargs):
        try:
            super().post(request, *args, **kwargs)
        except IntegrityError:
            messages.add_message(request, messages.ERROR,
                                 'This item is already present in the order ' +
                                 'If you want to change quantity, edit existing item')
            return redirect(reverse('orders_app:order', kwargs={'pk': self.request.GET["order_id"]}))

    def get_success_url(self):  # new
        return reverse('orders_app:order', kwargs={'pk': self.request.GET["order_id"]})

    def form_valid(self, form):
        #!!!!!!!!!!!!!!!!!!!!!!!
        form.instance.order = Order.objects.get(id=self.request.GET['order_id'])
        return super(OrderedItemCreateView, self).form_valid(form)


class ItemsList(ListView):
    model = Item
    template_name = 'orders_app/item_list.html'


class ItemCreateView(SuccessMessageMixin, CreateView):
    model = Item
    fields = ['name', 'price', 'category', 'unit']
    success_url = reverse_lazy('orders_app:items')
    success_message = 'Created new item!'


class ItemUpdateView(SuccessMessageMixin, UpdateView):
    model = Item
    fields = ['name', 'price', 'category', 'unit']
    success_url = reverse_lazy('orders_app:items')
    success_message = 'Updated item!'


class ItemDeleteView(DeleteView):
    model = Item
    fields = ['name', 'price', 'category', 'unit']

    def get_success_url(self):
        messages.success(self.request, 'Item deleted!')
        return reverse_lazy('orders_app:items')


class CustomersList(ListView):
    model = Customer
    template_name = 'orders_app/customer_list.html'


class CustomerCreateView(SuccessMessageMixin, CreateView):
    model = Customer
    fields = ['name']
    success_url = reverse_lazy('orders_app:customers')
    success_message = 'Customer created!'


class CustomerUpdateView(SuccessMessageMixin, UpdateView):
    model = Customer
    fields = ['name']
    success_url = reverse_lazy('orders_app:customers')
    success_message = 'Updated customer!'


class CustomerDeleteView(DeleteView):
    model = Customer
    fields = ['name']

    def get_success_url(self):
        messages.success(self.request, 'Customer deleted!')
        return reverse_lazy('orders_app:customers')


class CategoryCreateView(SuccessMessageMixin, CreateView):
    model = Category
    fields = ['name']

    def get_success_url(self) -> str:
        success_url: str
        next_url: str | None = self.request.GET.get('next', None)
        if next_url:
            success_url = next_url
        else:
            success_url = reverse_lazy('orders_app:categories')
        return success_url

    success_message = 'Category created!'


class CategoriesList(ListView):
    model = Category
    template_name = 'orders_app/category_list.html'


class CategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = Category
    fields = ['name']
    success_url = reverse_lazy('orders_app:categories')
    success_message = 'Updated category!'


class CategoryDeleteView(DeleteView):
    model = Category
    fields = ['name']

    def get_success_url(self):
        messages.success(self.request, 'Category deleted!')
        return reverse_lazy('orders_app:categories')
