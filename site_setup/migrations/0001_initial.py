# Generated by Django 4.1.1 on 2022-10-24 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSetupModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('logo', models.FileField(upload_to='images/logo')),
                ('mobile_1', models.CharField(max_length=20)),
                ('mobile_2', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=100)),
                ('whatsapp', models.CharField(max_length=100)),
                ('facebook', models.CharField(max_length=100)),
                ('instagram', models.CharField(max_length=100)),
                ('twitter', models.CharField(max_length=100)),
                ('address', models.TextField()),
            ],
        ),
    ]