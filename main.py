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
        self.__all_cards = {card["name"]: card for card in data["cards"]}

    def __str__(self):
        return f"{self.__all_cards}"

    @property
    def all_cards(self):
        return self.__all_cards


DECK = Deck()


class Card:
    def __init__(self, id_card: str):
        self.id_card = id_card
        data_card = DECK.all_cards.get(id_card, {})
        self.name = data_card.get("name", "")
        self.pile = data_card.get("pile", "")
        self.time = data_card.get("time", 0)
        self.picture = data_card.get("picture", "")
        self.daughters = data_card.get("daughters", [])
        self.limits = data_card.get("limits", [])
        self.rate = data_card.get("rate", 0)

    def __str__(self):
        return f"Card {self.id_card} with {self.daughters=}"


class Hand:
    """уже сыгранные карты"""

    def __init__(self, first_card):
        self.opened_cards = set()
        self.available_cards = {first_card}
        self.time_left = 0

    def play_card(self, id_card):
        card = Card(id_card)
        if card.id_card in self.available_cards:
            self.time_left += 0 if card.id_card in self.opened_cards else 1
            self.opened_cards.add(card.id_card)
            self.available_cards.update([_ for _ in card.daughters])
            print(f"Played {card}. Time left {self.time_left}")
            print(rf"dangerous_ties\{card.picture}")
            webbrowser.open(rf"dangerous_ties/{card.picture}")
        else:
            print(f"{card} not exist, available cards: {self.available_cards}")


if __name__ == "__main__":

    print(DECK)

    user_name = "goro"
    current_user = User(user_name)

    wanted_card = "i1"
    hand = Hand(wanted_card)

    while True:
        hand.play_card(wanted_card)

        print(hand.opened_cards)
        print(hand.available_cards)

        wanted_card = input("wanted card:").lower()
        if wanted_card == "exit":
            break
