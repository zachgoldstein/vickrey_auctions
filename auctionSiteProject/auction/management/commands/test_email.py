from auction.models import Auction, Bid
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Send test emails'

    def add_arguments(self, parser):
        parser.add_argument('-e', '--email_addresses', nargs='+', default=[])

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Sending test emails to {options['email_addresses']}"))
        for email_address in options['email_addresses']:
            print(f"email_address: {email_address}")
            send_mail(
                'Testing from local django',
                'Here is the message.',
                settings.EMAIL_FROM_ADDRESS,
                ['zachgold@gmail.com'],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f"Successfully sent test email to {email_address}"))

