# Generated by Django 4.1.1 on 2022-10-27 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_checkoutmodel_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkoutmodel',
            name='payment_method',
            field=models.CharField(default='online', max_length=20),
            preserve_default=False,
        ),
    ]
