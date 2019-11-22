from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from stdimage import JPEGField
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings


class Auction(models.Model):
    auction_id = models.CharField(max_length=32)
    active = models.BooleanField(default=True)

    AUCTION_CHOICES = [
        ('activate', 'Activate'),
        ('deactivate', 'Deactivate'),
        ('all sold', 'Mark Auction as Sold'),
    ]

    def __str__(self):
        return self.auction_id


class Category(models.Model):
    # Dependencies
    # auctionKey = models.ForeignKey(Auction, related_name='categories', on_delete=models.CASCADE)
    auction = models.ManyToManyField(Auction, related_name='categories')

    # Member Variables
    # Add child and parent categories here if we want them
    name = models.CharField(max_length=36)

    def __str__(self):
        return "%s category" % self.name


class Item(models.Model):
    # Dependencies
    auction = models.ForeignKey(Auction, related_name='items', on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='items_in_category')

    # Member Variables
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    current_price = models.DecimalField(max_digits=8, decimal_places=2)
    start_date = models.DateTimeField('start date')
    end_date = models.DateTimeField('end date')
    sold = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    picked_up = models.BooleanField(default=False)
    # winner = models.ForeignKey(Profile)

    def getTimeDiff(self):
        dif = self.end_date - timezone.now()
        if self.isSold():
            return "None"
        else:
            return "%s days, %s hours, %s minutes, and %s seconds" % \
                (dif.days, dif.seconds // 3600, (dif.seconds//60) % 60,
                    (dif.seconds//60)//60)

    def isSold(self):
        if (self.end_date - timezone.now()).total_seconds() < 0:
            self.sold = True
            self.whoWon()

        return self.sold

    def isActive(self):
        if self.auction.active:
            return True
        else:
            return False

    def getPrimaryImage(self):
        image_list = self.itemimage_set.order_by('pk')
        if len(image_list) > 0:
            return image_list[0].getImageThumbnail()
        else:
            return settings.MEDIA_URL + "/images/defaultItemImage.jpg"

    def whoWon(self):
        try:
            winner = self.bid_set.order_by('-price')[0].bidder
            # winner.setWon(self)
            return winner
        except (Exception):
            print(Exception)
            return None

    def __str__(self):
        return self.name


class Profile(models.Model):
    # Dependencies
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auctions = models.ManyToManyField(Auction)
    bid_on = models.ManyToManyField(Item)

    # Member Variables
    name = models.CharField(max_length=128)
    email = models.EmailField()
    phone_number = PhoneNumberField(blank=True)
    image = JPEGField(blank=True, upload_to='images/',
                      variations={'thumbnail': {"width": 300, "height": 300,
                                  "crop": True}},
                      delete_orphans=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def getImageThumbnail(self):
        if self.image:
            return self.image.thumbnail.url
        else:
            return settings.MEDIA_URL + "/images/defaultProfilePicture.jpg"

    def set_bid_on(self, item):
        if not self.bid_on.filter(pk=item.pk).exists():
            self.bid_on.add(item)
        return

    # def setWon(self, item):
    #     if not self.items_won.filter(pk=item.pk).exists():
    #         self.items_won.add(item)
    #     return

    def __str__(self):
        return self.name


class Bid(models.Model):
    # Dependencies
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)

    # Member Variables
    price = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField('Date published')

    def __str__(self):
        return "Bid for the item %s at the price of %s by the user %s" \
               % (self.item, self.price, self.bidder.username)


class ItemImage(models.Model):
    # Dependencies
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = JPEGField(upload_to='images/', variations={
        'thumbnail': {"width": 300, "height": 300, "crop": True}},
        delete_orphans=True)

    def getImageThumbnail(self):
        return self.image.thumbnail.url
