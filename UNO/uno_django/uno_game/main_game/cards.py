from .constants import COLOR, CARD


class Card:
    def __init__(self, color, body, type) -> None:
        self.color = color
        self.body = body
        self.type = type
     

    def copy(self):
        return Card(self.color, self.body, self.type)

    def __str__(self) -> str:
        return f"{[self.color]}{self.body}"
    
    def __repr__(self) -> str:
        return self.__str__()

