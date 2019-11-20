from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import EditProfile
import datetime
import socket
from django.conf import settings

from .models import Auction, Item, Bid


def index(request):
    return redirect('auctions:profile')


@login_required
def profile(request):
    if not request.user.profile.name or not request.user.profile.email:
        return redirect('auctions:editProfile')

    items_won_list = list()
    bid_on_list = list()
    user_items = request.user.profile.bid_on.order_by('end_date')

    for item in user_items:
        if item.isActive and not item.hidden:
            bid_on_list.append(item)

            if item.isSold():
                if item.whoWon() == request.user:
                    items_won_list.append(item)
                else:
                    pass

    # JAREN - CURRENTLY WORKING ON THIS
    # # # # #
    recentBidList = request.user.bid_set.order_by('-date')[:5]

    all_auctions_list = Auction.objects.filter().order_by('auction_id')
    # all_auctions_list = request.user.auction_set.order_by('auction_id')

    context = {
        'all_auctions_list': all_auctions_list,
        'recentBidList': recentBidList,
        'items_won_list': items_won_list,
        'bid_on_list': bid_on_list,
        }

    return render(request, 'auctions/profile.html', context)


@login_required
def explore(request):
    if not request.user.profile.name or not request.user.profile.email:
        return redirect('auctions:editProfile')

    all_auctions_list = Auction.objects.filter().order_by('auction_id')

    user_auctions = request.user.profile.auctions.all()

    context = {
        'all_auctions_list': all_auctions_list,
        'user_auctions': user_auctions,
    }
    return render(request, 'auctions/explore.html', context)


@login_required
def item(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)
    if not item.isActive:
        redirect(request.META.get('HTTP_REFERER'))

    EXTRA = 40
    TOTAL = 20
    shuffled_auction_extra = item.auction.items.order_by('?')[:EXTRA]

    shuffled_auction = list()
    for i in range(EXTRA):
        if len(shuffled_auction) > TOTAL or i >= len(shuffled_auction_extra):
            break
        if not shuffled_auction_extra[i].isSold() \
           and not shuffled_auction_extra[i].hidden \
           and not shuffled_auction_extra[i].pk == item.pk:
            shuffled_auction.append(shuffled_auction_extra[i])

    try:
        selected_bid = request.POST['bid']
        if item.isSold():
            raise KeyError("Item is sold")
    except (KeyError):
        bid_list = item.bid_set.order_by('-price')[:3]
        image_list = item.itemimage_set.order_by('pk')
        if len(image_list) > 0:
            primary_image = image_list[0].getImageThumbnail
        else:
            primary_image = settings.MEDIA_URL + "/images/defaultItemImage.jpg"
        return render(request, 'auctions/item.html', {
            'item': item,
            'bid_list': bid_list,
            'primary_image': primary_image,
            'image_list': image_list,
            'shuffled_auction': shuffled_auction,
            })
    else:
        if float(selected_bid) > item.current_price and not item.sold \
                                                    and not item.hidden:
            bid = Bid(item=item, bidder=request.user, price=selected_bid,
                      date=datetime.datetime.now())
            item.current_price = selected_bid  # TODO: Make a new bid
            request.user.profile.set_bid_on(item)
            bid.save()
            item.save()
            messages.success(request, 'Your $%s bid was successfully recorded.'
                             % item.current_price)
        else:
            messages.warning(request, 'Your $%s bid was ' % selected_bid +
                             'not recorded. An error happened while processing ' +
                             'your request.'
                             )

        return redirect('auctions:item', item.pk)


@login_required
def editProfile(request):
    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES or None,
                           instance=request.user.profile)
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
