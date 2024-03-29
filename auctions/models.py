from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from stdimage import JPEGField
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.utils.text import slugify
import itertools


class Auction(models.Model):
    auction_id = models.CharField(max_length=32)
    # slug = models.SlugField(
    #     editable=False,
    #     unique=True,
    #     verbose_name="Auction code"
    # )
    active = models.BooleanField(default=True)

    AUCTION_CHOICES = [
        ('activate', 'Activate'),
        ('deactivate', 'Deactivate'),
        ('all sold', 'Mark Auction as Sold'),
    ]

    # def _generate_slug(self):
    #     value = self.auction_id
    #     slug_candidate = slug_original = slugify(value, allow_unicode=True)
    #     for i in itertools.count(1):
    #         if not Auction.objects.filter(slug=slug_candidate).exists():
    #             break
    #         slug_candidate = '{}-{}'.format(slug_original, i)

    #     self.slug = slug_candidate

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self._generate_slug()

    #     super().save(*args, **kwargs)

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
        if not self.isOpen():
            return "Closed"
        else:
            return "%s days, %s hours, and %s minutes" % \
                (dif.days, dif.seconds // 3600, (dif.seconds//60) % 60)

    def isSold(self):
        if (self.end_date - timezone.now()).total_seconds() < 0:
            self.sold = True
            self.whoWon()

        return self.sold

    def isOpen(self):
        if (self.start_date - timezone.now()).total_seconds() > 0:
            return False
        elif self.isSold():
            return False
        else:
            return True

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
            self.current_price = self.bid_set.order_by('-price')[0].price
            # winner.setWon(self)
            return winner
        except (Exception):
            print(Exception)
            return None

    def getPrice(self):
        try:
            self.current_price = self.bid_set.order_by('-price')[0].price
            # winner.setWon(self)
            return self.current_price
        except (Exception):
            print(Exception)
            return self.current_price

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

    def get_name_and_pk(self):
        return '%s - %s' % (self.pk, self.username)

    User.add_to_class("__str__", get_name_and_pk)

    def __str__(self):
        return '%s - %s' % (self.name, self.pk)


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
