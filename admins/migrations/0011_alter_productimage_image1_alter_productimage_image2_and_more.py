# Generated by Django 4.2.2 on 2023-06-24 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0010_rename_image_productimage_image1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='images/products'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='images/products'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='images/products'),
        ),
    ]