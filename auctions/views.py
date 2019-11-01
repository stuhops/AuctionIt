from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .forms import EditProfile

from .models import Auction, Category, Item, Profile, Bid, ItemImage


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


def editProfile(request):
    if request.method == 'POST':
        form = EditProfile(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            print("Saved")
            return redirect('auctions:profile')

    else:
        form = EditProfile(instance=request.user.profile)

    return render(request, 'auctions/editProfile.html', {'profileForm': form})


def login(request):
    return render(request, 'auctions/login.html', {})
