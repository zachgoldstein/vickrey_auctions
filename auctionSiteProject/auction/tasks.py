from datetime import datetime, timedelta
import json

from celery import shared_task, Celery, Signature
from celery.utils.abstract import CallableSignature
from celery.schedules import crontab
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from auctionSiteProject.celery import app
from auction.models import Auction

from auction.services import complete_all_auctions_and_notify

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    print("running setup for periodic tasks...")
    # without celery_beat...

    # # Calls test('hello') every 10 seconds.
    # sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )

    # with celery beat....
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=10,
        period=IntervalSchedule.SECONDS,
    )
    PeriodicTask.objects.create(
        interval=schedule,                  # we created this above.
        name='Testing periodic task... test_task',          # simply describes this periodic task.
        task='test_task',  # name of task.
        args=json.dumps(['this is a test']),
        # kwargs=json.dumps({
        # 'be_careful': True,
        # }),
        # expires=datetime.utcnow() + timedelta(seconds=30,
        start_time = datetime.utcnow()
    )
    PeriodicTask.objects.create(
        interval=schedule,                  # we created this above.
        name='Testing periodic task... add_task',          # simply describes this periodic task.
        task='add_task',  # name of task.
        args=json.dumps([3, 8]),
        kwargs=json.dumps({
        }),
        expires=datetime.utcnow() + timedelta(seconds=30),
        start_time = datetime.utcnow()
    )

    schedule_min, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.MINUTES,
    )
    PeriodicTask.objects.create(
        interval=schedule_min,
        name='Complete active auctions',
        task='complete_auctions',
        args=json.dumps([]),
        start_time = datetime.utcnow()
    )

    print("ran setup periodic tasks...")

@app.task(name = "test_task")
def test(arg):
    print(arg)

@app.task(name = "add_task")
def add(x, y):
    z = x + y
    print(z)

# Find all active auctions that are expired and complete them
@app.task(name = "complete_auctions")
def auctions_complete():
    sent_emails = complete_all_auctions_and_notify()
    results = f"Attempted to complete auctions {Auction.have_completed.ids} and sent emails to {sent_emails}"
    print(results)
    return results

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