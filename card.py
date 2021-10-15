import webbrowser
from typing import List

from main import DECK


class Card:
    def __init__(self, id_card: str):
        data_card = DECK.all_cards.get(id_card, {})

        self.id_card: str = data_card.get("id_card", "")
        self.time: int = data_card.get("time", 0)
        self.daughters: List[str] = data_card.get("daughters", [])
        self.next_card: str = data_card.get("next_card", "")
        self.police: int = data_card.get("police", 0)

    def __str__(self):
        return f"{self.id_card=}, {self.time=}, {self.daughters=}, {self.next_card=}"

    def show_card(self):
        print(f"Played {self}.")
        webbrowser.open(rf"dangerous_ties/{self.id_card}.jpg")
