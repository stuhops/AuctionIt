from django.test import TestCase
from datetime import datetime, timedelta
from .models import Auction, Category, Item, Profile, Bid, ItemImage

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
        self.assertEqual(test_item.isSold(), False)

    def test_isSold(self):
        test_item = Item.objects.get(name="test_item2")
        test_item.isSold()
        self.assertEqual(test_item.isSold(), False)

    def test_getPrimaryImage(self):
        test_item = Auction.objects.get(auction_id="test_item1")
        self.assertEqual(str(test_item), "test_item1")

    def test_whoWon(self):
        test_item = Auction.objects.get(auction_id="test_item1")
        self.assertEqual(str(test_item), "test_item1")

    def test_item_class(self):
        test_item = Auction.objects.get(auction_id="test_item1")
        self.assertEqual(str(test_item), "test_item1")

class ProfileTestCase(TestCase):
    def setUp(self):
        Auction.objects.create(auction_id="test_item")

    def test_create_user_profile(self):
        test_item = Auction.objects.get(auction_id="test_item")
        self.assertEqual(str(test_item), "test_item")

    def test_save_user_profile(self):
        test_item = Auction.objects.get(auction_id="test_item")
        self.assertEqual(str(test_item), "test_item")

    def test_getImageThumbnail(self):
        test_item = Auction.objects.get(auction_id="test_item")
        self.assertEqual(str(test_item), "test_item")

    def test_set_bid_on(self):
        test_item = Auction.objects.get(auction_id="test_item")
        self.assertEqual(str(test_item), "test_item")

    def test_profile_class(self):
        test_item = Auction.objects.get(auction_id="test_item")
        self.assertEqual(str(test_item), "test_item")
class BidTestCase(TestCase):
    def setUp(self):
        Auction.objects.create(auction_id="test_item")

    def test_bid_class(self):
        test_item = Auction.objects.get(auction_id="test_item")
        self.assertEqual(str(test_item), "test_item")

class ItemImageTestCase(TestCase):
    def setUp(self):
        Auction.objects.create(auction_id="test_item")

    def test_ItemImage_class(self):
        test_item = Auction.objects.get(auction_id="test_item")
        self.assertEqual(str(test_item), "test_item")
