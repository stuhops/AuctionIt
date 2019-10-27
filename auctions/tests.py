from django.test import TestCase
from auctions.models import Auction, Category, Item, Person, Bid

# Create your tests here.


class AuctionTestCase(TestCase):
    def setUp(self):
        Auction.objects.create(auction_id="test_item")

    def test_action_class(self):
        test_item = Auction.objects.get(auction_id="test_item")
        self.assertEqual(print(test_item), "test_item")

class CategoryTestCase(TestCase):
    def setUp(self):
        Auction.objects.create(auction_id="test_item")

    def test_action_class(self):
        test_item = Auction.objects.get(auction_id="test_item")
        self.assertEqual(print(test_item), "test_item")
class ItemTestCase(TestCase):
    def setUp(self):
        Auction.objects.create(auction_id="test_item")

    def test_action_class(self):
        test_item = Auction.objects.get(auction_id="test_item")
        self.assertEqual(print(test_item), "test_item")
class PersonTestCase(TestCase):
    def setUp(self):
        Auction.objects.create(auction_id="test_item")

    def test_action_class(self):
        test_item = Auction.objects.get(auction_id="test_item")
        self.assertEqual(print(test_item), "test_item")
class BidTestCase(TestCase):
    def setUp(self):
        Auction.objects.create(auction_id="test_item")

    def test_action_class(self):
        test_item = Auction.objects.get(auction_id="test_item")
        self.assertEqual(print(test_item), "test_item")
