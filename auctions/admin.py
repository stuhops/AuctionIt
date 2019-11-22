from django.contrib import admin

from .models import *

def setActive(modeladmin, request, queryset):
    for auction in queryset:
        auction.active = True
        auction.save()
setActive.short_description = 'Activate the selected Auctions'

def setInactive(modeladmin, request, queryset):
    for auction in queryset:
        auction.active = False
        auction.save()
setInactive.short_description = 'Deactivate the selected Auctions'

def markAsSold(modeladmin, request, queryset):
    for auction in queryset:
      for item in auction.items:
        item.markAsSold()
        item.save()
markAsSold.short_description = 'PLEASE USE CAUTION Mark all items as sold in auction'


class AuctionAdmin(admin.ModelAdmin):
  list_display = ['auction_id', 'active']

  actions = [
    setActive,
    setInactive,
    markAsSold,
  ]


admin.site.register(Auction, AuctionAdmin)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Profile)
admin.site.register(Bid)
admin.site.register(ItemImage)
