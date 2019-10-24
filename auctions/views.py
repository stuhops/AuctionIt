from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("This is the index")


def profile(request):
    return HttpResponse("This is the user profile of user %s" % username)


def item(request):
    return HttpResponse("This is the item view of item %s" % item_id)


def login(request):
    return HttpResponse("This is the login")
