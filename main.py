import json
import webbrowser


class User:
    def __init__(self, id_t: str):
        self.id = id_t


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


class Card:
    @classmethod
    def get_card(cls, id_card: str):
        data_card = {
            "id_card": "i1",
            "time": 0,
            "daughters": [],
            "next_card": "",
            "up_time": 0,
            "police": 0,
            "rate": 0,
        }
        data_card.update(DECK.all_cards.get(id_card, {}))
        return data_card


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
        card = Card.get_card(id_card)

        if card["id_card"] in self.opened_cards:
            self.show_card(card)
            return

        if card["id_card"] not in self.available_cards:
            print(f"{card} not available, your next cards: {self.next_cards()}")
            return

        self.play_card(card)

        if card["police"]:
            card["next_card"] = self.police_cards.pop()
            self.available_cards.add(card["next_card"])

        if card["next_card"]:
            self.want_card(card["next_card"])

    def show_card(self, card):
        print(f"Played {card}. Time left {self.time_left}, police {self.police}")
        webbrowser.open(rf"dangerous_ties/{card['id_card']}.jpg")

    def play_card(self, card):
        self.time_left += card["time"]
        self.police += card["police"]
        self.opened_cards.add(card["id_card"])
        self.available_cards.update([_ for _ in card["daughters"]])

        self.show_card(card)


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
