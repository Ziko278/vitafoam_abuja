# Generated by Django 4.0.3 on 2022-10-31 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_productmodel_keys'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsizemodel',
            name='size',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
