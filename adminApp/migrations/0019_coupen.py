# Generated by Django 3.2 on 2022-02-03 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminApp', '0018_auto_20220202_0317'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupen_offer', models.IntegerField()),
                ('coupen_code', models.CharField(max_length=20, unique=True)),
            ],
        ),
    ]
