# Generated by Django 2.2.7 on 2019-11-22 21:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auto_20191122_1423'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='slug',
        ),
    ]
