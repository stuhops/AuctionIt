from django.contrib import admin
from django.utils import timezone

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

def markAllAsSold(modeladmin, request, queryset):
  for auction in queryset:
    for item in auction.items.all():
      item.sold = True

      item.end_date = timezone.now()
      if (item.end_date - item.start_date).total_seconds() < 0:
        item.start_date = item.end_date

      item.save()
markAllAsSold.short_description = 'CAUTION Mark all items as sold in auction'

def markAllAsOpen(modeladmin, request, queryset):
  for auction in queryset:
    for item in auction.items.all():
      item.sold = False

      item.start_date = timezone.now()
      if (item.end_date - item.start_date).total_seconds() < 0:
        item.end_date = item.start_date

      item.save()
markAllAsOpen.short_description = 'CAUTION Mark all items as open in auction'


class AuctionAdmin(admin.ModelAdmin):
  list_display = ['auction_id', 'active']

  actions = [
    setActive,
    setInactive,
    markAllAsSold,
    markAllAsOpen,
  ]


admin.site.register(Auction, AuctionAdmin)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Profile)
admin.site.register(Bid)
admin.site.register(ItemImage)
