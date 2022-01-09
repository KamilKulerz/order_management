from typing import Any
from django.db import models
from django.db.models import Count
from django.db.models.aggregates import Sum
from django.urls.base import reverse
from django_stubs_ext.aliases import ValuesQuerySet


class Customer(models.Model):

    name = models.CharField(max_length=50, blank=False, verbose_name="Name")
    # email = models.EmailField(blank=False)

    def __str__(self):
        return self.name

    def get_update_url(self) -> str:
        return reverse("orders_app:customers-update", kwargs={"pk": self.pk})

    def get_delete_url(self) -> str:
        return reverse("orders_app:customers-delete", kwargs={"pk": self.pk})


class Category(models.Model):

    name = models.CharField(max_length=50, blank=False, verbose_name="Name")

    def __str__(self):
        return self.name

    def get_update_url(self) -> str:
        return reverse("orders_app:categories-update", kwargs={"pk": self.pk})

    def get_delete_url(self) -> str:
        return reverse("orders_app:categories-delete", kwargs={"pk": self.pk})


class Item(models.Model):

    name = models.CharField(max_length=50, blank=False, verbose_name="Name")
    price = models.FloatField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    unit = models.CharField(max_length=50, blank=False)

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

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    status = models.CharField(
        max_length=50, blank=False, choices=ORDER_STATUSES)

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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['item', 'order'], name='unique item for order')
        ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50, blank=False, default='nok', choices=ITEM_STATUSES)
