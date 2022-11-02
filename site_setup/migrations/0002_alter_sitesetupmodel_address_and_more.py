# Generated by Django 4.1.1 on 2022-10-24 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_setup', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesetupmodel',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sitesetupmodel',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sitesetupmodel',
            name='facebook',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sitesetupmodel',
            name='instagram',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sitesetupmodel',
            name='logo',
            field=models.FileField(blank=True, null=True, upload_to='images/logo'),
        ),
        migrations.AlterField(
            model_name='sitesetupmodel',
            name='mobile_1',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='sitesetupmodel',
            name='mobile_2',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='sitesetupmodel',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='sitesetupmodel',
            name='twitter',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sitesetupmodel',
            name='whatsapp',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]