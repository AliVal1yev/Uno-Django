
from django.core.management.base import BaseCommand
from uno_game.models import Card
from uno_game.main_game.helpers import generate_deck

class Command(BaseCommand):
    help = "Imports UNO cards into the database"

    def handle(self, *args, **kwargs):
        deck = generate_deck()
        for card_data in deck:
            Card.objects.create(
                color=card_data.color,
                body=card_data.body,
                type=card_data.type
            )
        self.stdout.write(self.style.SUCCESS("Successfully imported UNO cards"))
