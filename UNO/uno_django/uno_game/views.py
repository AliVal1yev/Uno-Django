from django.shortcuts import render, get_object_or_404, redirect
from .models import Game, Player, Card, Table
from .forms import PlayCardForm, ColorChoiceForm
from .main_game.games import Uno
from .main_game.helpers import CARD, generate_deck
from django.core.exceptions import ValidationError




def next_player(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    # Update to the next player
    game.get_next_move()
    
    # Save the updated game state
    game.save()
    
    return redirect('game_view', game_id=game.id)


def game_view(request, game_id):
    game = Game.objects.get(id=game_id)
    current_player = game.get_current_player()
    
    
    if request.method == 'POST':
        form = PlayCardForm(request.POST)
        if form.is_valid():
            card = form.cleaned_data.get('card')
            draw_card = form.cleaned_data.get('draw_card')

            if draw_card:
                if game.deck.exists():
                    new_card = game.deck.first()
                    game.deck.remove(new_card)
                    current_player.hands.add(new_card)
                return redirect('game_view', game_id=game.id)

            if card:
                if game.table.check_card_validness(card):
                    game.table.add_card(card)
                    current_player.hands.remove(card)
                    
                    # Handle action cards
                    if card.type == 'ACTION':
                        if card.body == '⊘':  # Skip
                            game.reconstruct_order(action_type='⊘')
                            game.reset_turn()
                        elif card.body == '⇅':  # Reverse
                            game.reconstruct_order(action_type='⇅')
                            game.reset_turn()
                        elif card.body == '+2':  # Draw 2
                            next_player = game.get_next_player()
                            for _ in range(2):
                                if game.deck.exists():
                                    new_card = game.deck.first()
                                    game.deck.remove(new_card)
                                    next_player.hands.add(new_card)

                    elif card.type == 'WILD':
                        if card.body == '+4':
                            # Handle color change and draw 4 cards
                            ask_color(request, game)
                            for _ in range(4):
                                if game.deck.exists():
                                    new_card = game.deck.first()
                                    game.deck.remove(new_card)
                                    next_player = game.get_next_player()
                                    next_player.hands.add(new_card)
                        elif card.body == '⊕':
                            # Handle color change
                            ask_color(request, game)

                    if current_player.hands.count() == 0:
                        return render(request, 'uno_game/win.html', {'player': current_player})

                    game.get_next_move()
                    if game.turn >= len(game.players.all()):
                        game.reset_turn()
                        
                else:
                    form.add_error(None, "Invalid card. Please choose a valid card.")

    else:
        form = PlayCardForm()

    form.fields['card'].queryset = current_player.hands.all() 

    return render(request, 'uno_game/game.html', {
        'game': game,
        'current_player': current_player,
        'form': form,
    })


def ask_color(request, game):
    if request.method == 'POST':
        form = ColorChoiceForm(request.POST)
        if form.is_valid():
            selected_color = form.cleaned_data['color']
            # Implement logic to change the color for wild cards
            pass
        return redirect('game_view', game_id=game.id)
    else:
        form = ColorChoiceForm()
    return render(request, 'uno_game/color_choice.html', {'form': form})


def create_game(request):
    if request.method == 'POST':
        try:
            player_count = int(request.POST.get('player_count'))
            if player_count < 2:  # Ensure there are at least 2 players
                raise ValidationError("There must be at least 2 players.")
            
            player_names = [request.POST.get(f'player_{i}') for i in range(1, player_count + 1)]
            if len(set(player_names)) < player_count:  # Check for duplicate names
                raise ValidationError("Player names must be unique.")
            
            table = Table.objects.create()

            game = Game.objects.create(table=table)
            
            players = []
            for i, nickname in enumerate(player_names, start=1):
                player = Player.objects.create(nickname=nickname, order=i)
                players.append(player)
                game.players.add(player)
            
            deck_cards = Card.objects.all() 
            deck = generate_deck()
            for card in deck:
                card_instance = Card.objects.get(color=card.color, body=card.body, type=card.type)
                game.deck.add(card_instance)
            
            # Initialize the game (if needed)
            # game.start_game()

            return redirect('game_view', game_id=game.id)
        
        except ValidationError as e:
            return render(request, 'uno_game/create_game.html', {'error': str(e)})
        except Card.DoesNotExist:
            return render(request, 'uno_game/create_game.html', {'error': 'Some cards are missing in the database.'})
        except Exception as e:
            return render(request, 'uno_game/create_game.html', {'error': 'An error occurred while creating the game.'})

    return render(request, 'uno_game/create_game.html')





