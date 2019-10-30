from django.contrib import admin

from .models import Auction, Category, Item, Profile, Bid, ItemImage

admin.site.register(Auction)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Profile)
admin.site.register(Bid)
admin.site.register(ItemImage)
