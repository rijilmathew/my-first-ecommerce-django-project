# Generated by Django 4.2.2 on 2023-07-08 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0014_filter_price_product_filter_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_name', models.CharField(max_length=25)),
                ('code', models.CharField(max_length=25, unique=True)),
                ('valid_from', models.DateField()),
                ('valid_to', models.DateField()),
                ('discount_price', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]