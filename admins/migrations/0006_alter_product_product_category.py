# Generated by Django 4.2.2 on 2023-06-22 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0005_product_best_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_category',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='admins.productcategory'),
        ),
    ]