from django.db import models


class Auction(models.Model):
    auction_id = models.CharField(max_length=32)

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
    start_date = models.DateTimeField('start date')
    end_date = models.DateTimeField('end date')
    sold = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return "%s the item: (description) %s" % (self.name, self.description)


class Person(models.Model):
    # Dependencies
    # Member Variables
    name = models.CharField(max_length=128)
    # phone_number = PhoneField(blank=True, help_text='Contact phone number')  # https://pypi.org/project/django-phone-field/

    def __str__(self):
        return "This Person's name is %s" % self.name


class Bidder(models.Model):
    # Dependencies
    personal_info = models.OneToOneField(Person, on_delete=models.CASCADE)

    # Member Variables

    def __str__(self):
        return "This bidder's name is %s" % (self.personal_info.name)


class Bid(models.Model):
    # Dependencies
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    bidder = models.ForeignKey(Bidder, on_delete=models.CASCADE)

    # Member Variables
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return "Bid for the item %s at the price of %s by the user %s" \
               % (self.item, self.price, self.bidder.personal_info.name)




# TODO: Do we need to make an admin class or does it do that for us?


