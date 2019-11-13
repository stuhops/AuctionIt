# Generated by Django 2.2.6 on 2019-11-10 19:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import stdimage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auction_id', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=36)),
                ('auction', models.ManyToManyField(related_name='categories', to='auctions.Auction')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.IntegerField(default=None)),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=1000)),
                ('current_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('start_date', models.DateTimeField(verbose_name='start date')),
                ('end_date', models.DateTimeField(verbose_name='end date')),
                ('sold', models.BooleanField(default=False)),
                ('hidden', models.BooleanField(default=False)),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='auctions.Auction')),
                ('categories', models.ManyToManyField(related_name='items_in_category', to='auctions.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('image', stdimage.models.JPEGField(blank=True, upload_to='UploadedImages/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ItemImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', stdimage.models.JPEGField(upload_to='UploadedImages/')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date', models.DateTimeField(verbose_name='Date published')),
                ('bidder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.Item')),
            ],
        ),
    ]