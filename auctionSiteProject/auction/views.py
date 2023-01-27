from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from auction.models import Bid

from django.views.generic import ListView

class BidListView(ListView):
    model = Bid

def index(request):
    allBids = Bid.objects.all()

    template = loader.get_template('index.html')
    context = {
        'bids': allBids,
    }
    return HttpResponse(template.render(context, request))