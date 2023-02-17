from django.urls import path


from . import views
from auction.views import AuctionView, AuctionListView, AuctionCreateView
from auction.views import BidListView, BidCreateView

urlpatterns = [
    # path('', views.index, name='index'),
    path('', AuctionListView.as_view(), name='index'),
    path('bids/', BidListView.as_view()),
    path('bids/create', BidCreateView.as_view(), name="auction_create"),
    path('auctions/<int:pk>/', AuctionView.as_view(), name="auction_detail"),
    path('auctions', AuctionListView.as_view(), name="auction_list"),
    path('auctions/create', AuctionCreateView.as_view(), name="auction_create"),

    # testing out polling below
    path('auctions/testlive', views.liveUpdate, name='liveupdate'),
    path('auctions/dummyauction', views.dummyauction, name='dummyauction'),

    path('test-sl-post', views.dummyformreq, name='dummyformreq'),
    
]