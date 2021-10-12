from django.contrib import admin

# Register your models here.

from . import models
# Register your models here.


admin.site.register(models.Customer)
admin.site.register(models.Order)
admin.site.register(models.Item)
admin.site.register(models.OrderedItem)
admin.site.register(models.Category)


