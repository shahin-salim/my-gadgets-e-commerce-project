# Generated by Django 4.0.1 on 2022-01-10 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0003_alter_customuser_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='image',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
    ]