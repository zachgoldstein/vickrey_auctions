from django.db import models
from django.urls import reverse

import random

random_pics = [
    "https://picsum.photos/id/26",
    "https://picsum.photos/id/60",
    "https://picsum.photos/id/119",
    "https://picsum.photos/id/145",
]

class Auction(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    title = models.CharField(max_length=500, default="Empty Title")
    description = models.CharField(max_length=1000, default="Empty description")

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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Bid(models.Model):
    price = models.FloatField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, blank=True, null=True)
