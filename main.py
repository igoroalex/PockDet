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

    def __str__(self) -> str:
        return f"{self.id_card=}, {self.time=}, {self.daughters=}, {self.next_card=}"

    def show_card(self):
        print(f"Played {self}.")
        webbrowser.open(rf"dangerous_ties/{self.id_card}.jpg")


class Hand:
    """уже сыгранные карты"""

    def __init__(self, first_card: str):
        self.opened_cards = set()
        self.available_cards = {first_card}
        self.time_left = 0
        self.police = 0
        self.police_cards = ["p6", "p5", "p4", "p3", "p2", "p1"]
        self.last_card = ""
        self.jail = ""

    def next_cards(self) -> set:
        return self.available_cards - self.opened_cards

    def check_card(self, card: Card) -> bool:

        # ordinary conditions
        if card.id_card in self.opened_cards:
            card.show_card()
            return False

        if card.id_card not in self.available_cards:
            print(f"{card} not available, your next cards: {self.next_cards()}")
            return False

        # exceptional conditions
        if card.id_card == "s3" and self.time_left > 2:
            print(
                "Момент упущен. Полиция уже приехала и не допускает посторонних людей"
            )
            return False

        if card.id_card == "s4" and self.time_left > 5:
            card.daughters = []
            print("Соседи разошлись. не успели")
            return False

        if card.id_card == "c9" and self.last_card != "c8":
            print("Возможность подслушать упущена. Не стоило видимо уходить")
            return False

        if card.id_card == "h2" and self.time_left <= 4:
            card.police = 0

        if card.id_card == "f4" and (
            (14 <= self.time_left <= 22) or (38 <= self.time_left <= 46)
        ):
            card.next_card = "f6"
            self.available_cards.add(card.next_card)

        if card.id_card == "e2" and "h6" in self.opened_cards:
            card.police = 0
            card.next_card = "e3"
            self.available_cards.add(card.next_card)

        if self.jail == "p5":
            self.available_cards = {_ for _ in self.available_cards if _[0] != "c"}

        if self.jail == "p5" and card.id_card[0] == "c":
            print("Теперь вы не можете пользоваться помощью друзей в полиции")
            return False

        if card.id_card == "p5":
            self.jail = "p5"

        if card.police:
            card.next_card = self.police_cards.pop()
            self.available_cards.add(card.next_card)

        return True

    def want_card(self, id_card: str):
        card = Card(id_card)

        if self.check_card(card):
            self.play_card(card)

            if card.next_card:
                self.play_card(Card(card.next_card))

        return

    def play_card(self, card: Card):
        self.time_left += card.time
        self.police += card.police
        self.opened_cards.add(card.id_card)
        self.available_cards.update([_ for _ in card.daughters])
        self.last_card = card.id_card

        card.show_card()


if __name__ == "__main__":

    user_name = "goro"
    current_user = User(user_name)

    wanted_card = "i1"
    hand = Hand(wanted_card)

    while True:
        hand.want_card(wanted_card)

        print(hand.available_cards)

        wanted_card = input("wanted card:").lower()
        if wanted_card == "exit":
            break
