from constants import CARD


class Table:
    def __init__(self) -> None:
        self.content = [ ]

    def get_top_card(self):
        if self.content:
            return self.content[-1]
    
    def has_any_cards(self) -> bool:
        return bool(self.content)

    def add_card(self, card):
        self.content.append(card)

    def card_matches(self, player_card):
        last_card = self.get_top_card()
        color_matches = (player_card.color == last_card.color)
        body_matches = (player_card.body == last_card.body)
        match = (color_matches or body_matches)
        return match

    def check_card_validness(self, player_card) -> bool:
        is_wild_card = (player_card.type == CARD.WILD)
        return (is_wild_card or self.card_matches(player_card))
    
