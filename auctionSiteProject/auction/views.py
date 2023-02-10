from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from auction.models import Bid, Auction

from time import time

from django.views.generic import ListView, DetailView

class BidListView(ListView):
    model = Bid

class AuctionView(DetailView):
    model = Auction

class AuctionListView(ListView):
    model = Auction

def index(request):
    allBids = Bid.objects.all()

    template = loader.get_template('index.html')
    context = {
        'bids': allBids,
    }
    return HttpResponse(template.render(context, request))


# TEMP tesitng out polling below

def liveUpdate(request):
    # auctionID = request.GET.get("id", "0")
    auctionID = "1"

    template = loader.get_template('liveupdate.html')
    context = {
        "id": auctionID,
    }
    return HttpResponse(template.render(context, request))

def dummyauction(request):
    template = loader.get_template('dummyauction.html')

    auctionID = request.GET.get("id", "0")

    context = {
        "now": time(),
    }

    # if auction.expired:
    if auctionID == "1":
        return HttpResponse(template.render(context, request), status=286)
    else:
        return HttpResponse(template.render(context, request))
