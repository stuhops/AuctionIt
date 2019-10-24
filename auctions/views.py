from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Auction, Category, Item, Person, Bid


def index(request):
    return HttpResponse("This is the index")


def profile(request, username):
    template = loader.get_template('auctions/profile.html')
    context = {}
    return HttpResponse(template.render(context, request))


def item(request, item_id):
    template = loader.get_template('auctions/item.html')
    context = {}
    return HttpResponse(template.render(context, request))


def login(request):
    template = loader.get_template('auctions/login.html')
    context = {}
    return HttpResponse(template.render(context, request))
