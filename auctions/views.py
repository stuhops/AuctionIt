from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import EditProfile  # , JoinAuction
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
    wonTotal = 0
    wonItemsTotal = 0

    for item in user_items:
        if item.isActive() and not item.hidden:
            bid_on_list.append(item)

            if item.whoWon() == request.user:
                wonTotal += item.getPrice()

                if item.isSold():
                    items_won_list.append(item)
                    wonItemsTotal += 1

    recentBidList = request.user.bid_set.order_by('-date')[:3]

    all_auctions_list = Auction.objects.filter().order_by('auction_id')

    context = {
        'all_auctions_list': all_auctions_list,
        'recentBidList': recentBidList,
        'items_won_list': items_won_list,
        'bid_on_list': bid_on_list,
        'won_total': wonTotal,
        'won_items_total': wonItemsTotal,
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
    if not item.isActive or item.auction in request.user.profile.auctions.all():
        try: 
            redirect(request.META.get('HTTP_REFERER'))
        except (KeyError):
            redirect(explore)

    EXTRA = 40
    TOTAL = 20
    shuffled_auction_extra = item.auction.items.order_by('?')[:EXTRA]

    shuffled_auction = list()
    for i in range(EXTRA):
        if len(shuffled_auction) > TOTAL or i >= len(shuffled_auction_extra):
            break
        if shuffled_auction_extra[i].isOpen() \
           and not shuffled_auction_extra[i].pk == item.pk:
            shuffled_auction.append(shuffled_auction_extra[i])

    try:
        selected_bid = request.POST['bid']
        if item.isSold():
            raise KeyError("Item is sold")
    except (KeyError):
        if not item.isOpen():
            messages.warning(request,
                             'Alert: The bidding is currently \
                             closed for this item.'
                             )
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
        if float(selected_bid) > item.current_price and item.isOpen() \
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
            return redirect('auctions:profile')

    else:
        form = EditProfile(instance=request.user.profile)

    return render(request, 'auctions/editProfile.html', {'form': form})


@login_required
def codes(request):
    # get current ip address
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


@login_required
def join_auction(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = JoinAuction(request.POST)  # A form bound to the POST data
        if form.is_valid():
            form.save()
            return redirect('auctions:explore')
        # if form.is_valid() and Auction.objects.get(slug=form.slug):
        #     request.user.profile.auctions.append(
        #         Auction.objects.get(slug=form.slug)
        #     )
        #     messages.success(
        #         request, 'You have successfully been added to '
        #         + Auction.objects.get(slug=form.slug).auction_id
        #     )
        #     return redirect('auctions:explore')

    else:
        form = JoinAuction()

    return render(request, 'auctions/joinAuction.html', {"form": form})


@login_required
def live(request):
    return render(request, 'auctions/live.html', {"id": request.user.profile.pk})


@login_required
def winners(request):
    if not request.user.is_superuser:
        redirect('auctions:profile')
    else:
        all_items = list(Item.objects.all())
        item_list = list()

        for item in all_items:
            if item.isSold() and item.hidden is False:
                item_list.append(item)

        return render(request, 'auctions/winners.html', {"item_list": item_list})