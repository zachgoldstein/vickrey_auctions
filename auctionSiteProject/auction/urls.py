from django.urls import path

from . import views
from auction.views import BidListView, AuctionView

urlpatterns = [
    path('', views.index, name='index'),
    path('bids/', BidListView.as_view()),
    path('auctions/<int:pk>/', AuctionView.as_view()),
]