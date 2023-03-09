from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site
from django.conf import settings


import random
from statistics import fmean
from typing import List
from auction.vickrey import calculate_average_bid, calculate_top_n_average_bid, get_winning_bids, get_losing_bids, get_winning_price, get_recommendations

random_pics = [
    "https://picsum.photos/id/26",
    "https://picsum.photos/id/60",
    "https://picsum.photos/id/119",
    "https://picsum.photos/id/145",
]

class Bid(models.Model):
    price = models.FloatField()
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    auction = models.ForeignKey('Auction', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Bid(id={self.id}) price: {self.price} for Auction(id={self.auction.id}) from {self.email}"

class ActiveAuctionManager(models.Manager):
    def get_queryset(self):
        return super(ActiveAuctionManager, self).get_queryset().filter(
            status=Auction.StatusChoices.ACTIVE
        )

    def get_average_num_bids(self):
        auctions = self.get_queryset().all()
        return fmean([auction.bid_set.count() for auction in auctions])

# All auctions that are now complete and need to be updated
class HaveCompletedAuctionManager(models.Manager):
    def get_queryset(self):
        return super(HaveCompletedAuctionManager, self).get_queryset().filter(
            status=Auction.StatusChoices.ACTIVE,
            # check compete_date against current time
        )

    @property
    def ids(self):
        return [auction.id for auction in self.get_queryset()]

class Auction(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    active = ActiveAuctionManager()
    have_completed = HaveCompletedAuctionManager()

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    title = models.CharField(max_length=500, default="Empty Title")
    description = models.CharField(max_length=1000, default="Empty description")
    num_items = models.IntegerField(default=1)
    
    class StatusChoices(models.TextChoices):
        ACTIVE = 'ACT', _('Active')
        COMPLETE = 'CMP', _('Complete')
        INACTIVE = 'INACT', _('Inactive')

    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
    )

    @property
    def image_uri(self):
        return f"{random.choice(random_pics)}/400/400"

    @property
    def image_uri_large(self):
        return f"{random.choice(random_pics)}/1200/800"

    @property
    def relative_url(self):
        return reverse('auction_detail', args=[str(self.id)])
    
    @property
    def absolute_url(self):
        return f"http://{settings.DEFAULT_SITE_DOMAIN}{self.relative_url}"

    def __str__(self):
        return self.title

    @property
    def total_average_bid(self) -> float:
        return calculate_average_bid(list(self.bid_set.all()))

    @property
    def winning_average_bid(self) -> float:
        return calculate_top_n_average_bid(self.num_items, list(self.bid_set.all()))
    
    @property
    def recommendations(self) -> List[str]:
        return get_recommendations(self.num_items, list(self.bid_set.all()))
    
    @property
    def winning_bids(self) -> List[Bid]:
        return get_winning_bids(self.num_items, list(self.bid_set.all()))

    @property
    def losing_bids(self) -> List[Bid]:
        return get_losing_bids(self.num_items, list(self.bid_set.all()))

    @property
    def winning_bid_price(self) -> float:
        return get_winning_price(self.num_items, list(self.bid_set.all()))

    def complete(self):
        self.status = self.StatusChoices.COMPLETE
        self.save()
