# Generated by Django 4.0.1 on 2022-01-11 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminApp', '0005_products_product_name_alter_products_img1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='img1',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]