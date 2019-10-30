from django.contrib import admin

from .models import Auction, Category, Item, Person, Bid, ProfileImage, ItemImage

admin.site.register(Auction)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Person)
admin.site.register(Bid)
admin.site.register(ItemImage)
admin.site.register(ProfileImage)
