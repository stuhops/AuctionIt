from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse
from django.template import loader

from .models import Auction, Category, Item, Person, Bid


def index(request):
    return HttpResponse("This is the index")


def profile(request):
    # user = get_object_or_404(Person, username=username)

    # JAREN - CURRENTLY WORKING ON THIS
    # # # # #
    all_auctions_list = Auction.objects.filter().order_by('auction_id')
    context = {'all_auctions_list': all_auctions_list}
    return render(request, 'auctions/profile.html', context)
    # # # # #


def item(request, item_id):
    item = get_object_or_404(Item, item_id=item_id)
    return render(request, 'auctions/item.html', {'item': item})


def login(request):
    return render(request, 'auctions/login.html', {})
