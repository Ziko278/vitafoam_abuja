# Generated by Django 4.1.1 on 2022-10-27 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_ordermodel_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='status',
            field=models.CharField(default='pending', max_length=20),
            preserve_default=False,
        ),
    ]