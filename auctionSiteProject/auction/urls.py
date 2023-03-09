from django.urls import path


from . import views

# Auction views
from auction.views import AuctionView, AuctionListView, AuctionCreateView, AuctionSellerView, AuctionStatsView

# Bid views
from auction.views import BidListView, BidCreateView

# Application views
# from views import loginView

# JSON views
from auction.views import BidDataView

urlpatterns = [
    # path('', views.index, name='index'),
    path('', AuctionListView.as_view(), name='index'),
    path('bids/', BidListView.as_view()),
    path('bids/create', BidCreateView.as_view(), name="auction_create"),
    path('auctions/<int:pk>/', AuctionView.as_view(), name="auction_detail"),
    path('auctions/<int:pk>/seller', AuctionSellerView.as_view(), name="auction_detail_seller"),
    path('auctions/<int:pk>/stats', AuctionStatsView.as_view(), name="auction_detail_stats"),
    path('auctions', AuctionListView.as_view(), name="auction_list"),
    path('auctions/create', AuctionCreateView.as_view(), name="auction_create"),

    # Application views
    path('accounts/register/', views.register, name='login'),


    # JSON endpoint for auction chart data
    path('auctions/<int:pk>/prices', BidDataView.as_view(), name="auction_price_data"),

    # testing out polling below
    path('auctions/testlive', views.liveUpdate, name='liveupdate'),
    path('auctions/dummyauction', views.dummyauction, name='dummyauction'),

    path('test-sl-post', views.dummyformreq, name='dummyformreq'),
    
]