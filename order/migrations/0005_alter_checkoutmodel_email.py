# Generated by Django 4.1.1 on 2022-10-27 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_ordermodel_price_ordermodel_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkoutmodel',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
