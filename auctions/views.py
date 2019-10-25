from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse
from django.template import loader

from .models import Auction, Category, Item, Person, Bid


def index(request):
    return HttpResponse("This is the index")


def profile(request, username):
    # user = get_object_or_404(Person, username=username)
    return render(request, 'auctions/profile.html', {})


def item(request):
    # user = get_object_or_404(Item, item_id=item_id)
    return render(request, 'auctions/item.html', {})


def login(request):
    return render(request, 'auctions/login.html', {})
