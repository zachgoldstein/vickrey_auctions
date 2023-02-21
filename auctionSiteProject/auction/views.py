from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.http import QueryDict
from django.views.generic import ListView, DetailView
from django.views import View
from django.template import loader
from django.http import JsonResponse
from django.forms.models import model_to_dict

from time import time
from typing import cast, List

from auction.models import Bid, Auction


class BidListView(ListView):
    model = Bid

class BidCreateView(DetailView):
    model = Bid

    def post(self, request, *args, **kwargs):
        post = QueryDict(request.body) 
        print(post)       
        auction = Auction.objects.get(id=post["auction-id"])
        auction.bid_set.create(price=post["bid-value"])
        print(f"got auction with id: {auction.id}")

        print("created new bid")
        # return HttpResponse('POST request')
        template = loader.get_template('bid_confirmation.html')
        return HttpResponse(template.render({"bid":post["bid-value"]}, request))

class BidDataView(DetailView):
    model = Auction

    def get(self, request, *args, **kwargs):
        self.object = cast(Auction, self.get_object())
        return JsonResponse({"prices":[bid.price for bid in self.object.bid_set.all()]})

class AuctionView(DetailView):
    model = Auction

    # Intention is to only set a single field at once, for use by auto-updating inputs
    def put(self, request, *args, **kwargs):
        put = QueryDict(request.body)        
        auction = Auction.objects.get(id=put["id"])
        # Feels unsafe??? just use an allow-list of fields
        
        return_value = ""
        for field in Auction._meta.get_fields():
            if field.name in put and field.name is not "id":
                print(f"setting field {field.name} to {put[field.name]}")
                setattr(auction, field.name, put[field.name])
                return_value = put[field.name]
                break
        auction.save()
        print(f"put request, got auction, {auction}, returning {return_value}")
        return HttpResponse(return_value)

# Auction detail page for sellers
# - Can edit
# - Can add an update
# - Can view live stats (real heart of the application)
class AuctionSellerView(DetailView):
    model = Auction

    def get(self, request, *args, **kwargs):
        self.object = cast(Auction, self.get_object())
        
        context = self.get_context_data(object=self.object)

        template = loader.get_template('auction/auction_stats.html')
        return HttpResponse(template.render(context, request))


class AuctionListView(ListView):
    model = Auction

class AuctionCreateView(DetailView):
    model = Auction
    template_name = "auction/auction_create.html"

    def get_object(self):
        # Override to get a new, unsaved and empty model
        # the first input change will trigger the save on the new model
        obj = Auction()
        obj.save()
        print(f"auction id:{obj.id}")

        return obj

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


def dummyformreq(request: HttpRequest):
    print(f"request method: {request.method}")
    print(f"got a request, params:{request.POST}")
    return HttpResponse(200)

