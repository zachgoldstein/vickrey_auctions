# Create your tasks here

from auction.models import Auction

from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def count_auctions():
    return Auction.objects.count()


@shared_task
def rename_auction(auction_id, title):
    w = Auction.objects.get(id=auction_id)
    w.title = title
    w.save()