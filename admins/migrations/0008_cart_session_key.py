# Generated by Django 4.2.2 on 2023-06-23 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0007_product_product_quantity_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='session_key',
            field=models.CharField(default='', max_length=255),
        ),
    ]
