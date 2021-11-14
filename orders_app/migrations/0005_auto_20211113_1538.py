# Generated by Django 3.0.8 on 2021-11-13 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders_app', '0004_ordereditem_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={},
        ),
        migrations.AlterModelOptions(
            name='ordereditem',
            options={},
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('nok', 'Not started'), ('ong', 'Ongoing'), ('pkd', 'Packed'), ('shp', 'Shipped')], max_length=50),
        ),
        migrations.AlterField(
            model_name='ordereditem',
            name='status',
            field=models.CharField(choices=[('nok', 'Not started'), ('pro', 'Produces'), ('ass', 'Assembled'), ('pkd', 'Packed')], default='nok', max_length=50),
        ),
    ]