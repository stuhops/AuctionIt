from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .forms import EditProfile
import datetime

from .models import Auction, Item, Bid


def index(request):
    return redirect('auctions:profile')


def profile(request):
    try:
        if not request.user.profile.name or not request.user.profile.email:
            return redirect('auctions:editProfile')

        # JAREN - CURRENTLY WORKING ON THIS
        # # # # #
        all_auctions_list = Auction.objects.filter().order_by('auction_id')
        context = {'all_auctions_list': all_auctions_list}
        return render(request, 'auctions/profile.html', context)
        # # # # #
    except AttributeError:
        print("The user is not logged in")
        return redirect('login')


def item(request, item_id):
    item = get_object_or_404(Item, item_id=item_id)
    try:
        selected_bid = request.POST['bid']
    except (KeyError):
        bid_list = item.bid_set.order_by('-price')[:3]
        return render(request, 'auctions/item.html', {
            'item': item,
            'bid_list': bid_list,
            })
    else:
        if float(selected_bid) > item.current_price:
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
