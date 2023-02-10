from django.urls import path


from . import views
from auction.views import BidListView, AuctionView, AuctionListView

urlpatterns = [
    # path('', views.index, name='index'),
    path('', AuctionListView.as_view(), name='index'),
    path('bids/', BidListView.as_view()),
    path('auctions/<int:pk>/', AuctionView.as_view(), name="auction_detail"),
    path('auctions', AuctionListView.as_view(), name="auction_list"),

    # testing out polling below
    path('auctions/testlive', views.liveUpdate, name='liveupdate'),
    path('auctions/dummyauction', views.dummyauction, name='dummyauction'),
]