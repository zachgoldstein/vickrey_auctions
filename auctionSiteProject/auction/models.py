from django.db import models
from django.urls import reverse

import random

class Bid(models.Model):
    price = models.FloatField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

random_furniture_pics = [
    "https://api.lorem.space/image/furniture?w=400&h=400&hash=8B7BCDC2",
    "https://api.lorem.space/image/furniture?w=400&h=400&hash=500B67FB",
    "https://api.lorem.space/image/furniture?w=400&h=400&hash=A89D0DE6",
    "https://api.lorem.space/image/furniture?w=400&h=400&hash=225E6693",
    "https://api.lorem.space/image/furniture?w=400&h=400&hash=9D9539E7",
    "https://api.lorem.space/image/furniture?w=400&h=400&hash=BDC01094",
    "https://api.lorem.space/image/furniture?w=400&h=400&hash=7F5AE56A",
    "https://api.lorem.space/image/furniture?w=400&h=400&hash=4F32C4CF",
    "https://api.lorem.space/image/furniture?w=400&h=400&hash=B0E33EF4",
    "https://api.lorem.space/image/furniture?w=400&h=400&hash=2D297A22",
]

random_large_furniture_pics = []
for pic in random_furniture_pics:
    pic = pic.replace("w=400", "w=650")
    pic = pic.replace("h=400", "h=500")
    random_large_furniture_pics.append(pic)

class Auction(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    title = models.CharField(max_length=500, default="Empty Title")
    description = models.CharField(max_length=1000, default="Empty description")

    @property
    def image_uri(self):
        return random.choice(random_furniture_pics)

    @property
    def image_uri_large(self):
        return random.choice(random_large_furniture_pics)


    @property
    def absolute_url(self):
        return reverse('auction_detail', args=[str(self.id)])

    def __str__(self):
        return self.title

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)