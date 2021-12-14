from django.db import models
from django.urls.base import reverse

# Create your models here.
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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    unit = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.name


class OrderedItem(models.Model):

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50, blank=False, default='nok', choices=ITEM_STATUSES)

    # def __str__(self):
    #     return self.oiid
