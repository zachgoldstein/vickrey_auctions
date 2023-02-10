from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from auction.models import Bid, Auction

from django.views.generic import ListView, DetailView

class BidListView(ListView):
    model = Bid

class AuctionView(DetailView):
    model = Auction


def index(request):
    allBids = Bid.objects.all()

    template = loader.get_template('index.html')
    context = {
        'bids': allBids,
    }
    return HttpResponse(template.render(context, request))