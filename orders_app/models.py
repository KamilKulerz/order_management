from django.db import models
from django.db.models.aggregates import Sum
from django.urls.base import reverse
from django.db.models import Count


ORDER_STATUSES = [
    ('nok', 'Not started'),
    ('ong', 'Ongoing'),
    ('pkd', 'Packed'),
    ('shp', 'Shipped'),
]
ITEM_STATUSES = [
    ('nok', 'Not started'),
    ('pro', 'Produces'),
    ('ass', 'Assembled'),
    ('pkd', 'Packed'),
]


class Customer(models.Model):

    name = models.CharField(max_length=50, blank=False, verbose_name="Name")

    def __str__(self):
        return self.name

    def get_update_url(self):
        return reverse("orders_app:customers-update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("orders_app:customers-delete", kwargs={"pk": self.pk})


class Order(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50, blank=False, choices=ORDER_STATUSES)

    def __str__(self):
        return str(self.id)

    def get_ordered_items(self):
        items = [x.item for x in self.ordereditem_set.all()]
        return items

    @classmethod
    def count_orders(cls):
        return cls.objects.all().count()

    @classmethod
    def get_groupped_by_status(cls):
        return (Order.objects
                .values('status')
                .annotate(Count('status'))
                .order_by()
                )

    def count_items(self):
        return OrderedItem.objects.filter(order=self).count()

    def get_groupped_items_count(self):
        return (OrderedItem.objects
                .filter(order=self)
                .values('status')
                .annotate(Count('status'))
                .order_by())

    def get_groupped_items_sum(self):
        return (OrderedItem.objects
                .filter(order=self)
                .values('status')
                .annotate(Sum('quantity'))
                .order_by())


class Category(models.Model):

    name = models.CharField(max_length=50, blank=False, verbose_name="Name")

    def __str__(self):
        return self.name

    def get_update_url(self):
        return reverse("orders_app:categories-update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("orders_app:categories-delete", kwargs={"pk": self.pk})


class Item(models.Model):

    name = models.CharField(max_length=50, blank=False, verbose_name="Name")
    price = models.FloatField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    unit = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.name

    def get_update_url(self):
        return reverse("orders_app:items-update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("orders_app:items-delete", kwargs={"pk": self.pk})


class OrderedItem(models.Model):

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50, blank=False, default='nok', choices=ITEM_STATUSES)
