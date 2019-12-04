from django.test import TestCase
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from stdimage import JPEGField

from .models import Auction, Bid,Category, Item, ItemImage, Profile

# Create your tests here.


class AuctionTestCase(TestCase):
    def setUp(self):
        Auction.objects.create(auction_id="test_item")

    def test_action_class(self):
        test_item = Auction.objects.get(auction_id="test_item")
        self.assertEqual(str(test_item), "test_item")

class CategoryTestCase(TestCase):
    def setUp(self):
        Auction.objects.create(auction_id="test_item1")
        test_auction = Auction.objects.get(auction_id="test_item1")
        Category.objects.create(name="comedy")
        Category.objects.get(name="comedy").auction.add(test_auction)

    def test_category_class(self):
        test_auction = Category.objects.get(name="comedy")
        self.assertEqual(str(test_auction), "comedy category")
class ItemTestCase(TestCase):
    def setUp(self):
        Auction.objects.create(auction_id="test_item1")
        test_auction = Auction.objects.get(auction_id="test_item1")
        Category.objects.create(name="comedy")
        Category.objects.get(name="comedy").auction.add(test_auction)
        Item.objects.create(name="test_item2", current_price=420.69,start_date=datetime.now(),description="This is the current description for the test item class",end_date=(datetime.now() + timedelta(days=1)),auction=test_auction)
        #Item.objects.get(name="test_item2").description.add("This is the current description for the test item class")
        Item.objects.get(name="test_item2").sold=False
        Item.objects.get(name="test_item2").picked_up=False


    def test_getTimeDiff_class(self):
        test_item = Item.objects.get(name="test_item2")
        dif = test_item.end_date - timezone.now()
        time = "%s days, %s hours, %s minutes, and %s seconds" % \
                (dif.days, dif.seconds // 3600, (dif.seconds//60) % 60)
        self.assertEqual(test_item.isSold(), False)
        self.assertEqual(test_item.getTimeDiff(),time)

    def test_isSold(self):
        test_item = Item.objects.get(name="test_item2")
        self.assertEqual(test_item.isSold(), False)
        test_item = Item.objects.get(name="test_item2")
        test_item.sold = True
        self.assertEqual(test_item.isSold(), True)

    def test_isActive(self):
        test_item = Item.objects.get(name="test_item2")
        self.assertEqual(test_item.isActive(), True)

    def test_getPrimaryImage(self):
        test_item = Item.objects.get(name="test_item2")
        self.assertEqual(str(test_item), "test_item2")

    def test_whoWon(self):
        test_item = Item.objects.get(name="test_item2")
        self.assertEqual(test_item.whoWon(), None)

    def test_item_class(self):
        test_item = Item.objects.get(name="test_item2")
        self.assertEqual(str(test_item), "test_item2")

class ProfileTestCase(TestCase):
    def setUp(self):
        Auction.objects.create(auction_id="test_item1")
        test_auction = Auction.objects.get(auction_id="test_item1")
        Category.objects.create(name="comedy")
        Category.objects.get(name="comedy").auction.add(test_auction)
        Item.objects.create(name="test_item2", current_price=420.69,start_date=datetime.now(),description="This is the current description for the test item class",end_date=(datetime.now() + timedelta(days=1)),auction=test_auction)
        Item.objects.get(name="test_item2").sold=False
        Item.objects.get(name="test_item2").picked_up=False
        test_user = User(username="test_user",first_name="Test",last_name="User", email="test@testemail.com", password="password")
        test_user.save()

    def test_getImageThumbnail(self):
        test_profile = User.objects.get(username="test_user").profile
        test_profile.image = ""
        self.assertEqual(test_profile.getImageThumbnail(), "/media//images/defaultProfilePicture.jpg")
        test_profile.image = "/media/"
        self.assertEqual(test_profile.getImageThumbnail(), "/media/media/.thumbnail.jpeg")

    def test_set_bid_on(self):
        test_profile = User.objects.get(username="test_user").profile
        test_item = Item.objects.get(name="test_item2")
        test_profile.set_bid_on(test_item)
        self.assertEqual(str(test_profile.bid_on.order_by("end_date")[0]), "test_item2")

    def test_profile_class(self):
        test_profile = User.objects.get(username="test_user").profile
        test_profile = "test_user"
        self.assertEqual(str(test_profile), "test_user")

class BidTestCase(TestCase):
    def setUp(self):
        Auction.objects.create(auction_id="test_item1")
        test_auction = Auction.objects.get(auction_id="test_item1")
        Category.objects.create(name="comedy")
        Category.objects.get(name="comedy").auction.add(test_auction)
        Item.objects.create(name="test_item2", current_price=420.69,start_date=datetime.now(),description="This is the current description for the test item class",end_date=(datetime.now() + timedelta(days=1)),auction=test_auction)
        Item.objects.get(name="test_item2").sold=False
        Item.objects.get(name="test_item2").picked_up=False
        test_item =Item.objects.get(name="test_item2")
        test_user = User.objects.create_user(username="test_user",first_name="Test",last_name="User", email="test@testemail.com", password="password")
        Bid.objects.create(item=test_item,bidder=test_user,price="125.99", date=datetime.now())

    def test_bid_class(self):
        test_item = Item.objects.get(name="test_item2")
        test_bid = Bid.objects.get(item=test_item)
        self.assertEqual(str(test_bid), "Bid for the item test_item2 at the price of 125.99 by the user test_user")
        self.assertEqual(str(test_bid.price),'125.99')

class ItemImageTestCase(TestCase):
    def setUp(self):
        Auction.objects.create(auction_id="test_item1")
        test_auction = Auction.objects.get(auction_id="test_item1")
        Category.objects.create(name="comedy")
        Category.objects.get(name="comedy").auction.add(test_auction)
        Item.objects.create(name="test_item2", current_price=420.69,start_date=datetime.now(),description="This is the current description for the test item class",end_date=(datetime.now() + timedelta(days=1)),auction=test_auction)
        #Item.objects.get(name="test_item2").description.add("This is the current description for the test item class")
        Item.objects.get(name="test_item2").sold=False
        Item.objects.get(name="test_item2").picked_up=False
        test_item =Item.objects.get(name="test_item2")
        ItemImage.objects.create(item=test_item,image="")

    def test_ItemImage_class(self):
        test_item =Item.objects.get(name="test_item2")
        test_item_image = ItemImage.objects.get(item=test_item, image= JPEGField())
        self.assertEqual(test_item_image.getImageThumbnail(), "test_item")
