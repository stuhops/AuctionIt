from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from stdimage import StdImageField, JPEGField
from phonenumber_field.modelfields import PhoneNumberField

class Auction(models.Model):
    auction_id = models.CharField(max_length=32)

    def __str__(self):
        return self.auction_id


class Category(models.Model):
    # Dependencies
    auction = models.ManyToManyField(Auction)

    # Member Variables
    # Add child and parent categories here if we want them
    name = models.CharField(max_length=36)

    def __str__(self):
        return "%s category" % self.name


class Item(models.Model):
    # Dependencies
    auction = models.ForeignKey(Auction, related_name='items', on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)

    # Member Variables
    item_id = models.IntegerField(default=None)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    current_price = models.DecimalField(max_digits=8, decimal_places=2)
    start_date = models.DateTimeField('start date')
    end_date = models.DateTimeField('end date')
    sold = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)


    def getTimeDiff(self):
        dif = self.end_date.replace(tzinfo=None) - datetime.datetime.now()
        return "%s days, %s hours, %s minutes, and %s seconds" % (dif.days, dif.seconds // 3600, (dif.seconds//60)%60, (dif.seconds//60)//60)

    def __str__(self):
        return "%s the item: (description) %s" % (self.name, self.description)


class Profile(models.Model):
    # Dependencies
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Member Variables
    name = models.CharField(max_length=128)
    email = models.EmailField()
    phone_number = PhoneNumberField(blank=True)
    image = JPEGField(blank=True, upload_to='UploadedImages/', variations={'thumbnail': {"width": 100, "height": 100, "crop": True}})

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.name


class Bid(models.Model):
    # Dependencies
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)

    # Member Variables
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return "Bid for the item %s at the price of %s by the user %s" \
               % (self.item, self.price, self.bidder.personal_info.name)


class ItemImage(models.Model):
    # Dependencies
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = JPEGField(upload_to='UploadedImages/', variations={'thumbnail': {"width": 100, "height": 100, "crop": True}})
