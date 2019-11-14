# Generated by Django 2.2.7 on 2019-11-14 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20191113_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='items_won',
            field=models.ManyToManyField(related_name='items_won', to='auctions.Item'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bid_on',
            field=models.ManyToManyField(related_name='bid_on', to='auctions.Item'),
        ),
    ]
