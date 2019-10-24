from django.db import models


class Auction(models.Model):
    auction_id = models.CharFile(max_length=32)

    def __str__(self):
        return "%s the auction" % self.auction_id


class Category(models.Model):
    # Dependencies
    auction = models.ManyToManyField(Auction)

    # Member Variables
    # Add child and parent categories here if we want them
    name = models.CharField(max_length=36)

    def __str__(self):
        return "%s the category" % self.name


class Item(models.Model):
    # Dependencies
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)

    # Member Variables
    description = models.CharField(max_length=1000)
    current_price = models.DecimalField(max_digits=8, decimal_places=2)
    sold = models.BooleanField(default=False)
    hidden = models.BooleanFiled(default=False)

    def __str__(self):
        return "%s the item: (description) %s" % (self.name, self.description)


class Bid(models.Model):
    # Dependencies
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    bidder = models.ForeignKey(Bidder, on_delete=models.CASCADE)

    # Member Variables
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return "Bid for the item %s at the price of %s by the user %s" \
                % (self.item, self.price, self.bidder.personal_info.name)


class Bidder(models.Model):
    # Dependencies
    personal_info = models.OneToOneField(Person)

    # Member Variables


class Person(models.Model):
    # Dependencies
    # Member Variables
    name = models.CharField(max_length = 128)
    phone_number = PhoneField(blank=True, help_text='Contact phone number')  # https://pypi.org/project/django-phone-field/


# TODO: Do we need to make an admin class or does it do that for us?
