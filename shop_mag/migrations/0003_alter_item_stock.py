# Generated by Django 4.2 on 2023-04-24 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_mag', '0002_item_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='stock',
            field=models.IntegerField(),
        ),
    ]
