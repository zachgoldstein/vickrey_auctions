from django.urls import path

from . import views
from auction.views import BidListView

urlpatterns = [
    path('', views.index, name='index'),
    path('bids/', BidListView.as_view()),
]