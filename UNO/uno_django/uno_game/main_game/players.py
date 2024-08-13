class Player:
    def __init__(self, nickname, order) -> None:
        self.nickname = nickname
        self.order = order
        self.hands = [ ]

    def __str__(self) -> str:
        return f"{self.nickname}"
    
    def __repr__(self) -> str:
        return self.__str__()

    @property
    def hand_is_empty(self) -> bool:
        return (not self.hands)

    def add_card(self, cards):
        is_list = isinstance(cards, list)
        if is_list:
            self.hands.extend(cards)
        else:
            self.hands.append(cards)

    def get_card(self, idx):
        return self.hands[idx]
    
    def remove_card(self, card):
        self.hands.remove(card)
