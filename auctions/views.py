from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Auction, Category, Item, Person, Bid


def index(request):
    return HttpResponse("This is the index")


def profile(request, username):
    return render(request, 'auctions/profile.html', {})


def item(request, item_id):
    return render(request, 'auctions/item.html', {})


def login(request):
    return render(request, 'auctions/login.html', {})
