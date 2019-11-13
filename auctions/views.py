from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import EditProfile
import datetime
import socket

from .models import Auction, Item, Bid


def index(request):
    return redirect('auctions:profile')


@login_required
def profile(request):
    try:
        if not request.user.profile.name or not request.user.profile.email:
            return redirect('auctions:editProfile')

        # JAREN - CURRENTLY WORKING ON THIS
        # # # # #
        recentBidList = request.user.bid_set.order_by('-date')[:5]

        all_auctions_list = Auction.objects.filter().order_by('auction_id')
        # all_auctions_list = request.user.auction_set.order_by('auction_id')

        context = {
            'all_auctions_list': all_auctions_list,
            'recentBidList': recentBidList,
            }

        return render(request, 'auctions/profile.html', context)
        # # # # #
    except AttributeError:
        print("The user is not logged in")
        return redirect('login')


@login_required
def explore(request):
    try:
        if not request.user.profile.name or not request.user.profile.email:
            return redirect('auctions:editProfile')

        all_auctions_list = Auction.objects.filter().order_by('auction_id')

        active_auction = request.session.get('clicked_auction')
        # No idea what I'm doing, apparently.

        context = {
            'all_auctions_list': all_auctions_list,
            'active_auction': active_auction,
        }
        return render(request, 'auctions/explore.html', context)
    
    except AttributeError:
        print("The user is not logged in")
        return redirect('login')


@login_required
def item(request, item_id):
    item = get_object_or_404(Item, item_id=item_id)
    item.isSold()

    try:
        selected_bid = request.POST['bid']
        if item.sold:
            raise KeyError("Item is sold")
    except (KeyError):
        bid_list = item.bid_set.order_by('-price')[:3]
        return render(request, 'auctions/item.html', {
            'item': item,
            'bid_list': bid_list,
            })
    else:
        if float(selected_bid) > item.current_price and not item.sold and not item.hidden:
            bid = Bid(item=item, bidder=request.user, price=selected_bid,
                      date=datetime.datetime.now())
            item.current_price = selected_bid  # TODO: Make a new bid
            bid.save()
            item.save()
            messages.success(request, 'Your $%s bid was successfully recorded.'
                             % item.current_price)
        else:
            messages.error(request, 'Your $%s bid was ' % selected_bid +
                           'not recorded. An error happened while processing ' +
                           'your request.'
                           )

        return redirect('auctions:item', item.item_id)


@login_required
def editProfile(request):
    if request.method == 'POST':
        form = EditProfile(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            print("Saved")
            return redirect('auctions:profile')

    else:
        form = EditProfile(instance=request.user.profile)

    return render(request, 'auctions/editProfile.html', {'form': form})


@login_required
def codes(request):
    # get current ip adress
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ipAdress = s.getsockname()[0]
    s.close()

    # get port
    port = request.META['SERVER_PORT']

    # get Item list
    items = Item.objects.all()

    return render(request, 'auctions/codes.html', {
        "ipAdress": ipAdress,
        "port": port,
        "items": items,
    })
