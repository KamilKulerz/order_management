# Generated by Django 3.0.8 on 2021-12-11 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders_app', '0006_auto_20211211_1234'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='customer_id',
            new_name='customer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
        migrations.CreateModel(
            name='OrderedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('status', models.CharField(choices=[('nok', 'Not started'), ('pro', 'Produces'), ('ass', 'Assembled'), ('pkd', 'Packed')], default='nok', max_length=50)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders_app.Item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders_app.Order')),
            ],
        ),
    ]