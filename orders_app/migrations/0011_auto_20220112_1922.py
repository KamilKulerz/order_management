# Generated by Django 3.2.10 on 2022-01-12 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders_app', '0010_ordereditem_unique item for order'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='item',
            constraint=models.CheckConstraint(check=models.Q(('price__gte', 0)), name='price > 0'),
        ),
        migrations.AddConstraint(
            model_name='ordereditem',
            constraint=models.CheckConstraint(check=models.Q(('quantity__gte', 0)), name='qty > 0'),
        ),
    ]
