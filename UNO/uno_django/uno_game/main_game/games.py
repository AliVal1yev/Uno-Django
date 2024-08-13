# from .constants import CARD, COLOR
# from .cards import Card
# class Uno:
#     START_CARD_COUNT = 7

#     def __init__(self, players: list) -> None:
#         self.turn = 0
#         self.moves_count = 0
#         self.players = players

#     def first_move(self) -> bool:
#         return self.moves_count == 0

#     def get_current_player(self):
#         return self.players[self.turn]
    
#     def get_next_move(self):
#         self.turn += 1
#         if self.turn == len(self.players):
#             self.reset_turn()
#         self.moves_count += 1

#     def get_next_player(self):
#         self.get_next_move()
#         if self.turn == len(self.players):
#             self.reset_turn()
#         return self.players[self.turn]
        

#     def change_color(self, card):
#         new_color = input("Enter color for the wild card: ")
#         if new_color in COLOR.MAIN_COLORS:
#             card_copy = card.copy()
#             card_copy.color = new_color
#             return card_copy
#         else:
#             print("Please enter a correct color!")
#             return False


#     def reset_turn(self) -> None:
#         self.turn = 0

#     def reconstruct_order(self, action_type) -> None:
#         idx = self.turn
#         players = self.players

#         if action_type == CARD.ACTION_SKIP_BODY:
#             players += players[:idx]
#             players = players[idx:]
#             self.players = players
#         elif action_type == CARD.ACTION_REVERSE_BODY:
#             left = players[:idx+1] 
#             left.reverse() 
#             right = players[idx+1:]
#             right.reverse()
#             self.players = left + right

from uno_game.models import Card, Game, Player

class Uno:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.turn = game.turn
        self.players = list(game.players.all())
        self.direction = game.direction

    def first_move(self) -> bool:
        return self.game.deck.count() == 0  # Adjust based on your game logic

    def get_current_player(self) -> Player:
        return self.game.current_player

    def get_next_move(self):
        self.turn = (self.turn + (1 if self.direction else -1)) % len(self.players)
        self.game.turn = self.turn
        self.game.save()

    def get_next_player(self) -> Player:
        self.get_next_move()
        return self.players[self.turn]

    def change_color(self, card: Card):
        # Implement color change logic
        pass

    def reset_turn(self) -> None:
        self.turn = 0
        self.game.turn = self.turn
        self.game.save()

    def reconstruct_order(self, action_type: str) -> None:
        if action_type == '⊘':  # Skip
            self.get_next_move()  # Skip next player
        elif action_type == '⇅':  # Reverse
            self.direction = not self.direction
            self.game.direction = self.direction
            self.game.save()
        elif action_type == '+2':  # Draw 2
            next_player = self.get_next_player()
            for _ in range(2):
                if self.game.deck.exists():
                    new_card = self.game.deck.first()
                    self.game.deck.remove(new_card)
                    next_player.hands.add(new_card)
            next_player.save()

    def handle_wild_card(self, card: Card):
        # Implement wild card logic
        pass