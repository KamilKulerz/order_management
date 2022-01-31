from typing import Any
from django.db import models
from django.db.models import Count
from django.db.models.aggregates import Sum
from django.db.models.query_utils import Q
from django.urls.base import reverse
from django_stubs_ext.aliases import ValuesQuerySet
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class Customer(models.Model):

    name = models.CharField(max_length=50, blank=False, verbose_name=_("Name"))
    # email = models.EmailField(blank=False)

    def __str__(self):
        return self.name

    def get_update_url(self) -> str:
        return reverse("orders_app:customers-update", kwargs={"pk": self.pk})

    def get_delete_url(self) -> str:
        return reverse("orders_app:customers-delete", kwargs={"pk": self.pk})


class Category(models.Model):

    name = models.CharField(max_length=50, blank=False, verbose_name=_("Name"))

    def __str__(self):
        return self.name

    def get_update_url(self) -> str:
        return reverse("orders_app:categories-update", kwargs={"pk": self.pk})

    def get_delete_url(self) -> str:
        return reverse("orders_app:categories-delete", kwargs={"pk": self.pk})


class Item(models.Model):

    name = models.CharField(max_length=50, blank=False, verbose_name=_("Name"))
    price = models.FloatField(blank=True, verbose_name=_("Price"))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name=_("Category"))
    unit = models.CharField(max_length=50, blank=False, verbose_name=_("Unit"))

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(price__gte=0), name='price > 0')
        ]

    def clean(self):
        if self.price < 0:
            raise ValidationError({'price': _('Price must be greater than 0')})

    def __str__(self):
        return self.name

    def get_update_url(self) -> str:
        return reverse("orders_app:items-update", kwargs={"pk": self.pk})

    def get_delete_url(self) -> str:
        return reverse("orders_app:items-delete", kwargs={"pk": self.pk})


class Order(models.Model):
    ORDER_STATUSES = [
        ('nok', 'Not started'),
        ('ong', 'Ongoing'),
        ('pkd', 'Packed'),
        ('shp', 'Shipped'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, verbose_name=_("Customer"))
    status = models.CharField(
        max_length=50, blank=False, choices=ORDER_STATUSES, verbose_name=_("Status"))

    def __str__(self) -> str:
        return str(self.id)

    def get_ordered_items(self) -> list[Item]:
        items = [x.item for x in self.ordereditem_set.all()]
        return items

    @classmethod
    def count_orders(cls) -> int:
        return cls.objects.all().count()

    @classmethod
    def get_groupped_by_status(cls) -> 'ValuesQuerySet[Order, dict]':
        return (Order.objects
                .values('status')
                .annotate(Count('status'))
                .order_by()
                )

    def count_items(self):
        return OrderedItem.objects.filter(order=self).count()

    def get_groupped_items_count(self) -> 'ValuesQuerySet[OrderedItem, dict]':
        return (OrderedItem.objects
                .filter(order=self)
                .values('status')
                .annotate(Count('status'))
                .order_by())

    def get_groupped_items_sum(self) -> 'ValuesQuerySet[OrderedItem, dict]':
        return (OrderedItem.objects
                .filter(order=self)
                .values('status')
                .annotate(Sum('quantity'))
                .order_by())


class OrderedItem(models.Model):
    ITEM_STATUSES = [
        ('nok', 'Not started'),
        ('pro', 'Produces'),
        ('ass', 'Assembled'),
        ('pkd', 'Packed'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name=_("Item"))
    quantity = models.IntegerField(blank=False, verbose_name=_("Quantity"))
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_("Order"))
    status = models.CharField(
        max_length=50, blank=False, default='nok', choices=ITEM_STATUSES, verbose_name=_("Status"))

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['item', 'order'], name='unique item for order'),
            models.CheckConstraint(check=Q(quantity__gte=0), name='qty > 0')
        ]

    def clean(self):
        if self.quantity < 0:
            raise ValidationError({'quantity': _('Quantity must be greater than 0')})
