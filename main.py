import json
import webbrowser
from typing import Final


class User:
    def __init__(self, id_t: str):
        self.id = id_t


class Deck:
    """при инициализации программы (не сессии)
    записать данные всех карт из json в базу данных"""

    def __init__(self):
        with open("dangerous_ties.json", "r") as file:
            data = json.load(file)
        self.__all_cards = data

    def __str__(self):
        return f"{self.__all_cards}"

    @property
    def all_cards(self):
        return self.__all_cards


DECK: Final = Deck()


class Card:
    def __init__(self, id_card: str):
        data_card = DECK.all_cards.get(id_card, {})
        self.id_card = data_card.get("id_card", "")
        self.time = data_card.get("time", 0)
        self.daughters = data_card.get("daughters", [])
        self.next_card = data_card.get("next_card", "")
        self.up_time = data_card.get("up_time", 0)
        self.police = data_card.get("police", 0)
        self.rate = data_card.get("rate", 0)

    def show_card(self):
        print(f"Played {self}.")
        webbrowser.open(rf"dangerous_ties/{self.id_card}.jpg")


class Hand:
    """уже сыгранные карты"""

    def __init__(self, first_card):
        self.opened_cards = set()
        self.available_cards = {first_card}
        self.time_left = 0
        self.police = 0
        self.police_cards = ["p6", "p5", "p4", "p3", "p2", "p1"]

    def next_cards(self):
        return self.available_cards - self.opened_cards

    def want_card(self, id_card):
        card = Card(id_card)

        if card.id_card in self.opened_cards:
            card.show_card()
            return

        if card.id_card not in self.available_cards:
            print(f"{card} not available, your next cards: {self.next_cards()}")
            return

        self.play_card(card)

        if card.police:
            card.next_card = self.police_cards.pop()
            self.available_cards.add(card.next_card)

        if card.next_card:
            self.want_card(card.next_card)

    def play_card(self, card: Card):
        self.time_left += card.time
        self.police += card.police
        self.opened_cards.add(card.id_card)
        self.available_cards.update([_ for _ in card.daughters])

        card.show_card()


if __name__ == "__main__":

    # print(DECK)

    user_name = "goro"
    current_user = User(user_name)

    wanted_card = "i1"
    hand = Hand(wanted_card)

    while True:
        hand.want_card(wanted_card)

        # print(hand.opened_cards)
        print(hand.available_cards)

        wanted_card = input("wanted card:").lower()
        if wanted_card == "exit":
            break
