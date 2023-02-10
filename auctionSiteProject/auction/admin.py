from django.contrib import admin

from .models import Bid, Auction

admin.site.register(Bid)
admin.site.register(Auction)
