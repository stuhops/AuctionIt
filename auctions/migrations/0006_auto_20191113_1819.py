# Generated by Django 2.2.7 on 2019-11-14 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20191113_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bid_on',
            field=models.ManyToManyField(to='auctions.Item'),
        ),
    ]
