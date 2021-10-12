from django.db import models

# Create your models here.
class Customer(models.Model):
    class Meta:
        verbose_name = 'Klient'
        verbose_name_plural = 'Klienci'

    name = models.CharField(max_length=50, blank=False, verbose_name="Name")

    def __str__(self):
        return self.name


class Order(models.Model):
    class Meta:
        verbose_name = 'Zamówienie'
        verbose_name_plural = 'Zamowienia'

    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return str(self.id)

class Category(models.Model):
    class Meta:
        verbose_name = 'Kategoria'
        verbose_name_plural = 'Kategorie'
    name = models.CharField(max_length=50, blank=False, verbose_name="Name")

    def __str__(self):
        return self.name

class Item(models.Model):
    class Meta:
        verbose_name = 'Towar'
        verbose_name_plural = 'Towary'

    name = models.CharField(max_length=50, blank=False, verbose_name="Name")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    unit = models.CharField(max_length=50, blank=False)
    
    def __str__(self):
        return self.name

class OrderedItem(models.Model):
    class Meta:
        verbose_name = 'ZamówionyTowar'
        verbose_name_plural = 'ZamówioneTowary'
    # id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.oiid

