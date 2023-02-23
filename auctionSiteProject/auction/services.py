# Core business logic

from auction.models import Auction, Bid
from typing import List
from django.core.mail import send_mail
from django.conf import settings
from smtplib import SMTPException

def complete_auction_and_notify(auction:Auction) -> List[str]:
    sent_emails = []

    if not auction.email:
        print(f"No email found for seller auction {auction.id}, returning")
        return sent_emails

    # Send email to seller
    seller_text = f"""
        Your auction, {auction.title}, at {auction.absolute_url} is complete. 
        There were {auction.bid_set.count()} bids
        The winning bid price was ${auction.winning_bid_price:.2f}, and average winning bid was ${auction.winning_average_bid:.2f}
    """
    try:
        send_mail(
            'Your Auction for {auction.title} Complete',
            seller_text,
            settings.EMAIL_FROM_ADDRESS,
            [auction.email],
            fail_silently=False,
        )
        sent_emails.append(auction.email)
    except SMTPException as e:
        print(f"A SMTPException exception occurred sending an email: {e}")
    except Exception as e:
        print(f"A exception occurred sending an email: {e}")

    # send notifications emails to all winning bids
    for bid in auction.winning_bids:
        if not bid.email:
            print(f"No email found for bid {bid.id}")
            continue
        try:
            winning_bid_text = f"""
                You won the auction, {auction.title}, at {auction.absolute_url}. 
                You won with a bid of ${bid.price:.2f}, the auction price is going to be ${auction.winning_bid_price:.2f}
                So you pay ${bid.price - auction.winning_bid_price:0.2f} less than you offered to pay
                Please contact the seller at {auction.email} for transfer instructions.
            """
            send_mail(
                'You won the auction for {auction.title}!',
                winning_bid_text,
                settings.EMAIL_FROM_ADDRESS,
                [bid.email],
                fail_silently=False,
            )
            sent_emails.append(bid.email)
        except SMTPException as e:
            print(f"A SMTPException exception occurred sending an email: {e}")
        except Exception as e:
            print(f"A exception occurred sending an email: {e}")

    # send notifications emails to all losing bids
    for bid in auction.losing_bids:
        if not bid.email:
            print(f"No email found for bid {bid.id}")
            continue
        try:
            losing_bid_text = f"""
                You lost the auction, {auction.title}, at {auction.absolute_url}. 
                You lost with a bid of ${bid.price:.2f}
            """
            send_mail(
                'You lost the auction for {auction.title}!',
                losing_bid_text,
                settings.EMAIL_FROM_ADDRESS,
                [bid.email],
                fail_silently=False,
            )
            sent_emails.append(bid.email)
        except SMTPException as e:
            print(f"A SMTPException exception occurred sending an email: {e}")
        except Exception as e:
            print(f"A exception occurred sending an email: {e}")

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
