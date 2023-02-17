from django.db import models
from django.urls import reverse
from typing import List

import random
from auction.vickrey import calculate_average_bid, calculate_top_n_average_bid, get_winning_bids, get_winning_price, get_recommendations

random_pics = [
    "https://picsum.photos/id/26",
    "https://picsum.photos/id/60",
    "https://picsum.photos/id/119",
    "https://picsum.photos/id/145",
]

class Bid(models.Model):
    price = models.FloatField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    auction = models.ForeignKey('Auction', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Bid({self.id}) price: {self.price} for auction {self.auction.id}"

class Auction(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    title = models.CharField(max_length=500, default="Empty Title")
    description = models.CharField(max_length=1000, default="Empty description")
    num_items = models.IntegerField(default=1)

    @property
    def image_uri(self):
        return f"{random.choice(random_pics)}/400/400"

    @property
    def image_uri_large(self):
        return f"{random.choice(random_pics)}/1200/800"

    @property
    def absolute_url(self):
        return reverse('auction_detail', args=[str(self.id)])

    def __str__(self):
        return self.title

    def calculate_total_average_bid(self) -> float:
        return calculate_average_bid(list(self.bid_set.all()))

    def calculate_winning_average_bid(self) -> float:
        return calculate_top_n_average_bid(self.num_items, list(self.bid_set.all()))
    
    @property
    def recommendations(self) -> List[str]:
        return get_recommendations(list(self.bid_set.all()))
    
    @property
    def winning_bids(self) -> List[Bid]:
        return get_winning_bids(self.num_items, list(self.bid_set.all()))

    @property
    def winning_bid_price(self) -> float:
        return get_winning_price(self.num_items, list(self.bid_set.all()))


    # def calculate_top_average_bids(self) -> float:
    #     # find n top auction.num_items bids
    #     return calculate_average_bid(self.num_items, self.bid_set)

    # def get_winning_bid(self) -> Bid:
    #     get_winning_bid(self.num_items, self.bid_set)
    #     self.bid_set.get()
