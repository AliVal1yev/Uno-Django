import os

from helpers import generate_deck
from constants import CARD
from players import Player
from tables import Table
from games import Uno


deck = generate_deck()
table = Table()
players = [ ]
game = Uno(players)


count = int(input("Enter player count >> "))
for pl in range(1, count+1):
    nickname = input(f"Nickname {pl}:\n")

    player = Player(
        nickname=nickname,
        order=pl
    )
    players.append(player)

def ask_color():
    modified_card = game.change_color(player_card)
    table.add_card(modified_card)

def draw_card(player):
    card = deck.pop()
    player.add_card(card)
    clear()
    print(table.get_top_card())
    print(f"{player}'s hand after drawing a card:")
    for n, card in enumerate(player.hands, start=1):
        print(f"{n}. {card}")


def next_move():
    game.get_next_move()
    if game.turn == len(players):
        game.reset_turn()


def check_choice(choice):
    if choice == "0":
        draw_card(current_player)
        choice = input("Enter number or 'n' to next player>> ")

    if choice == 'n':
        next_move()
        return True
    elif choice == "0":
        input("You already draw a card!!!")
        next_move()
        return True
    
    elif choice.isdigit():
        return int(choice)
    
    else:
        print("Please enter a number or 'n'")
        return None

        
def distribute_cards(): 
    for pl in players:
        for _ in range(7):
            card = deck.pop()
            pl.add_card(card)

distribute_cards()

def clear():
    os.system("cls")

first_card = list(filter(lambda c: (c.type == CARD.NUMERIC), deck))[0]
table.add_card(first_card)
deck.remove(first_card)

while True:
    clear()

    print(table.get_top_card())

    current_player = game.get_current_player()
    input(f"{current_player}'s turn. Gozlerinizi yumun!")

    for n, card in enumerate(current_player.hands, start=1):
        print(f"{n}. {card}")
    choice = input("Enter number or 0 to draw card>> ")

    result = check_choice(choice)
    if result is True:
        continue
    elif result is None:
        continue
        
    idx = result - 1
    if not 0 <= idx <= len(current_player.hands)-1:
        input("Enter valid number")
        continue
    player_card = current_player.get_card(idx)

    is_valid_card = table.check_card_validness(player_card)

    if is_valid_card:
        table.add_card(player_card)
        current_player.remove_card(player_card)
    else:
        input("Enter an appropriate card")
        continue

    if player_card.type == CARD.ACTION:

        if player_card.body == CARD.ACTION_SKIP_BODY:
            game.reconstruct_order(action_type=CARD.ACTION_SKIP_BODY)
            game.reset_turn() 
            game.get_next_move() 

        elif player_card.body == CARD.ACTION_REVERSE_BODY:
            game.reconstruct_order(action_type=CARD.ACTION_REVERSE_BODY)
            game.reset_turn()

        elif player_card.body == CARD.ACTION_DRAW_2_BODY:
            random_cards = [ ]
            for _ in range(2):
                card = deck.pop()
                random_cards.append(card)      
            next_player = game.get_next_player()
            next_player.add_card(random_cards)
            

    elif player_card.type == CARD.WILD:
        
        if player_card.body == CARD.WILD_DRAW_4_BODY:
            ask_color()
            random_cards = [ ]
            for _ in range(4):
                card = deck.pop()
                random_cards.append(card)
            next_player = game.get_next_player()
            next_player.add_card(random_cards)
        
        elif player_card.body == CARD.WILD_UNIVERSAL:
            ask_color()

    if current_player.hand_is_empty:
        print(f"{current_player} wins!")
        break

    game.get_next_move()
    if game.turn == len(game.players):
        game.reset_turn()
    
