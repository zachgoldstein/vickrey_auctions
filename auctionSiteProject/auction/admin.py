from django.contrib import admin

from .models import Bid, Auction

# admin.site.register(Bid)
# admin.site.register(Auction)

class BidInline(admin.TabularInline):
    model = Bid

class AuctionAdmin(admin.ModelAdmin):
    inlines = [
        BidInline,
    ]

admin.site.register(Auction, AuctionAdmin) 
admin.site.register(Bid)