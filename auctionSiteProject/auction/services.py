# Core business logic

from auction.models import Auction, Bid
from typing import List
from django.core.mail import send_mail
from smtplib import SMTPException

def complete_auction_and_notify(auction:Auction) -> List[str] :
    # send notifications to all winning bids and return the emails that were notified
    sent_emails = []

    try:
        send_mail(
            'Subject here',
            'Here is the message.',
            'from@example.com',
            ['to@example.com'],
            fail_silently=False,
        )
    except SMTPException as e:
        print(f"A SMTPException exception occurred sending an email: {e}")
    except Exception as e:
        print(f"A exception occurred sending an email: {e}")

    # send notifications to all losing bids
    # send notifications to seller

    auction.complete()

    return sent_emails

def complete_all_auctions_and_notify() -> List[str]:
    # complete all active auctions, collect sent emails and return list
    sent_emails = []
    auctions: List[Auction] = Auction.active.all()
    for auction in auctions:
        auction_sent_emails = complete_auction_and_notify(auction)
        sent_emails.extend(auction_sent_emails)
    
