# Generated by Django 3.2 on 2022-02-02 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminApp', '0017_alter_category_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='variantandprice',
            name='final_price',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='products',
            name='offer',
            field=models.IntegerField(default=0),
        ),
    ]
