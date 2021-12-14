import json
from typing import Final


class Deck:
    """при инициализации программы (не сессии)
    записать данные всех карт из json в базу данных"""

    def __init__(self):
        self.name = "dangerous_ties"

        with open(f"{self.name}.json", "r") as file:
            data = json.load(file)
        self.__all_cards = data

    def __str__(self):
        return f"{self.__all_cards}"

    @property
    def all_cards(self):
        return self.__all_cards

    @staticmethod
    def start_investigation():
        return "i1"

    @staticmethod
    def finish_investigation():
        return "m1"

    @staticmethod
    def police_cards():
        return ["p6", "p5", "p4", "p3", "p2", "p1"]

    def get_data_card(self, id_card: str):
        return self.all_cards.get(id_card, {})


DECK: Final = Deck()
