from typing import List

from auction.models import Auction, Bid
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist, Obj

from auction.services import complete_all_auctions_and_notify, complete_auction_and_notify
from auction.models import Auction


class Command(BaseCommand):
    help = 'Completes a set of auctions. If auction_ids is used, just complete those auctions, otherwise complete all'

    def add_arguments(self, parser):
        parser.add_argument('auction_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        print(f"auction_ids: {options['auction_ids']}")
        sent_emails: List[str] = []
        completed_auctions: List[str] = []
        if len(options['auction_ids']) > 0:
            for auction_id in options['auction_ids']:
                try:
                    auction = Auction.objects.get(id=auction_id)
                    auction_sent_emails = complete_auction_and_notify(auction)
                    sent_emails.extend(auction_sent_emails)
                    completed_auctions.append(auction.id)
                except(ObjectDoesNotExist):
                    self.stdout.write(self.style.ERROR(f"Could not find auction with id {auction_id}"))
            self.stdout.write(self.style.SUCCESS(f"Attempted to complete auctions {completed_auctions} and sent emails to {sent_emails}"))
            return

        if len(options['auction_ids']) == 0:
            active_auctions = Auction.active.all()
            if len() == 0:
                self.stdout.write(self.style.ERROR(f"No active auctions found"))
            else:
                # This could gobble up some errors if some auctions fail to complete
                auction_sent_emails = complete_all_auctions_and_notify()
                sent_emails.extend(auction_sent_emails)
                active_auctions_ids = [auction.id for auction in active_auctions]
                self.stdout.write(self.style.SUCCESS(f"Attempted to complete all active auctions {active_auctions_ids} and sent emails to {sent_emails}"))
            return

