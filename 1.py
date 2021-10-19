import json


class Deck:
    """при инициализации программы (не сессии)
    записать данные всех карт из json в базу данных"""

    def __init__(self):
        with open("dangerous_ties.json", "r") as file:
            data = json.load(file)
        self.__all_cards = {card["id_card"]: card for card in data["cards"]}

    def __str__(self):
        return f"{self.__all_cards}"

    @property
    def all_cards(self):
        return self.__all_cards


DECK = Deck()

with open("dangerous_ties.json", "w") as file:
    json.dump(DECK.all_cards, file)

