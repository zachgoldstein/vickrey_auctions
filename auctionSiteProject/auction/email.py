from smtplib import SMTPException
from django.core.mail import send_mail
from django.conf import settings
from typing import List

from auction.models import Auction, Bid

def send_seller_email(auction: Auction) -> str:
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
        return auction.email
    except SMTPException as e:
        print(f"A SMTPException exception occurred sending an email: {e}")
    except Exception as e:
        print(f"A exception occurred sending an email: {e}")

def send_winning_bid_email(auction: Auction, bid:Bid) -> str:
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
        return bid.email
    except SMTPException as e:
        print(f"A SMTPException exception occurred sending an email: {e}")
    except Exception as e:
        print(f"A exception occurred sending an email: {e}")

def send_losing_bid_email(auction: Auction, bid: Bid) -> str:
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
        return bid.email
    except SMTPException as e:
        print(f"A SMTPException exception occurred sending an email: {e}")
    except Exception as e:
        print(f"A exception occurred sending an email: {e}")

