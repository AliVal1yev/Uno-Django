from django.db import models
from .main_game.helpers import generate_deck
from .main_game.constants import COLOR, CARD

class Card(models.Model):
    COLOR_CHOICES = [
        ('blue', 'Blue'),
        ('yellow', 'Yellow'),
        ('red', 'Red'),
        ('green', 'Green'),
        ('black', 'Black'),
    ]
    CARD_TYPES = [
        ('NUMERIC', 'Numeric'),
        ('ACTION', 'Action'),
        ('WILD', 'Wild'),
    ]

    color = models.CharField(max_length=20, choices=COLOR_CHOICES)
    body = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=CARD_TYPES)

    def __str__(self):
        return f"{self.color} {self.body}"

class Player(models.Model):
    nickname = models.CharField(max_length=50)
    order = models.PositiveIntegerField()
    hands = models.ManyToManyField(Card, blank=True, related_name='players')

    def __str__(self):
        return self.nickname

    def hand_is_empty(self):
        return not self.hands.exists()

class Table(models.Model):
    content = models.ManyToManyField(Card, blank=True)

    def get_top_card(self):
        return self.content.order_by('id').last() if self.content.exists() else None


    def has_any_cards(self):
        return self.content.exists()

    def add_card(self, card):
        self.content.add(card)
        print(f"Cards on table after adding: {self.content.all()}")  # Debugging line


    def card_matches(self, player_card):
        last_card = self.get_top_card()
        if not last_card:
            return False
        return (player_card.color == last_card.color) or (player_card.body == last_card.body)

    def check_card_validness(self, player_card):
        return player_card.type == 'WILD' or self.card_matches(player_card)

class Game(models.Model):
    players = models.ManyToManyField(Player)
    current_player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, related_name='current_games')
    table = models.OneToOneField(Table, on_delete=models.CASCADE)
    deck = models.ManyToManyField(Card, related_name='deck_cards')
    turn = models.PositiveIntegerField(default=0)
    direction = models.BooleanField(default=True)  # True for forward, False for reverse

    def get_current_player(self):
        return self.current_player
    
    
    def get_next_player(self):
        players_list = list(self.players.all())
        if not players_list:
            return None
        current_index = players_list.index(self.current_player)
        if self.direction: 
            next_index = (current_index + 1) % len(players_list)
        else:
            next_index = (current_index - 1) % len(players_list)
        self.current_player = players_list[next_index]
        self.save()
        return self.current_player


    def get_next_move(self):
        self.get_next_player()  
        self.save()


    def reset_turn(self):
        self.turn = 0

    def reconstruct_order(self, action_type):
        # Convert ManyToManyManager to list
        players_list = list(self.players.all())
        if not players_list:
            return
        
        # Find the current player index
        current_index = players_list.index(self.current_player)

        if action_type == CARD.ACTION_SKIP_BODY:
            self.turn = (self.turn + 1) % len(players_list)
        
        elif action_type == CARD.ACTION_REVERSE_BODY:
            players_list.reverse()
            self.players.set(players_list)
            self.turn = (len(players_list) - 1 - current_index) % len(players_list)
        self.save()
    
    def __str__(self) -> str:
        return f'{self.pk}'
    
    def start_game(self):
        self.deal_cards_to_players()

    def deal_cards_to_players(self):
        for player in self.players.all():
            for _ in range(7):
                if self.deck.exists():
                    card = self.deck.first()
                    self.deck.remove(card)
                    player.hands.add(card)
            player.save()
    
