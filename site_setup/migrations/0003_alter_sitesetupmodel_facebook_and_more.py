# Generated by Django 4.1.1 on 2022-10-24 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_setup', '0002_alter_sitesetupmodel_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesetupmodel',
            name='facebook',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sitesetupmodel',
            name='instagram',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sitesetupmodel',
            name='twitter',
            field=models.URLField(blank=True, null=True),
        ),
    ]
