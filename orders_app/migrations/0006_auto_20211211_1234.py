# Generated by Django 3.0.8 on 2021-12-11 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders_app', '0005_auto_20211113_1538'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='category_id',
            new_name='category',
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='orders_app.Item'),
        ),
        migrations.DeleteModel(
            name='OrderedItem',
        ),
    ]
