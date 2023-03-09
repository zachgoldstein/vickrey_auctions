# Core business logic

from auction.models import Auction, Bid
from typing import List
from django.conf import settings

from auction.email import send_losing_bid_email, send_seller_email, send_winning_bid_email

def complete_auction_and_notify(auction:Auction) -> List[str]:
    sent_emails = []

    if not auction.email:
        print(f"No email found for seller auction {auction.id}, returning")
        return sent_emails

    seller_email = send_winning_bid_email(auction)
    sent_emails.append(seller_email)

    # send notifications emails to all winning bids
    for bid in auction.winning_bids:
        if not bid.email:
            print(f"No email found for bid {bid.id}")
            continue
        winning_email = send_winning_bid_email(auction, bid)
        sent_emails.append(winning_email)

    # send notifications emails to all losing bids
    for bid in auction.losing_bids:
        if not bid.email:
            print(f"No email found for bid {bid.id}")
            continue
        losing_email = send_losing_bid_email(auction, bid)
        sent_emails.append(losing_email)

    auction.complete()
    return sent_emails

def complete_all_auctions_and_notify() -> List[str]:
    # complete all active auctions, collect sent emails and return list
    sent_emails = []
    auctions: List[Auction] = Auction.have_completed.all()
    for auction in auctions:
        auction_sent_emails = complete_auction_and_notify(auction)
        sent_emails.extend(auction_sent_emails)
    return sent_emails
