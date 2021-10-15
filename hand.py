from typing import Set, List

from card import Card


class Hand:
    """уже сыгранные карты"""

    def __init__(self, first_card: str):
        self.opened_cards: Set[str] = set()
        self.available_cards: Set[str] = {first_card}
        self.time_left: int = 0
        self.police: int = 0
        self.police_cards: List[str] = ["p6", "p5", "p4", "p3", "p2", "p1"]
        self.last_card: str = ""
        self.jail: str = ""
        self.rate: int = 0

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
            self.available_cards = {
                _ for _ in self.available_cards if not _.startswith("c")
            }

        if self.jail == "p5" and card.id_card.startswith("c"):
            print("Теперь вы не можете пользоваться помощью друзей в полиции")
            return False

        if card.id_card == "p5":
            self.jail = "p5"

        if card.id_card == "p6":
            self.jail = "p6"

        if card.id_card == "m2" and self.jail == "p6":
            self.rate += 5
            card.next_card = "m10"
            card.daughters.append(card.next_card)

        if card.id_card == "m4" and self.jail == "p6":
            self.rate += 7
            card.next_card = "m10"
            card.daughters.append(card.next_card)

        if card.id_card == "m5" and self.jail == "p6":
            self.rate += 15
            card.next_card = "m10"
            card.daughters.append(card.next_card)

        if card.id_card == "m6" and self.jail == "p6":
            self.rate += 9
            card.next_card = "m10"
            card.daughters.append(card.next_card)

        if card.id_card == "m7":
            self.rate += 100
            self.rate -= sum(
                [
                    20
                    for _ in self.opened_cards
                    if _ in ("m2", "m4", "m5", "m6", "m8", "m9")
                ]
            )
            self.rate -= self.time_left
            self.rate -= 10 if self.jail == "p6" else 0

        if card.id_card == "m8" and self.jail == "p6":
            self.rate += 65
            self.rate -= sum(
                [
                    20
                    for _ in self.opened_cards
                    if _.startswith("m") and _ not in ("m1", "m3", "m8")
                ]
            )
            self.rate -= self.time_left
            card.next_card = "m10"
            card.daughters.append(card.next_card)

        if card.id_card == "m9" and self.jail == "p6":
            self.rate += 70
            self.rate -= sum(
                [
                    20
                    for _ in self.opened_cards
                    if _.startswith("m") and _ not in ("m1", "m3", "m9")
                ]
            )
            self.rate -= self.time_left
            card.next_card = "m10"
            card.daughters.append(card.next_card)

        if card.id_card == "m10":
            print(f"Ваш результат: {self.rate}")

        if card.id_card == "p10":
            print("!!!Поздравляю!!!")

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

    def play_card(self, card: Card):
        self.time_left += card.time
        self.police += card.police
        self.opened_cards.add(card.id_card)
        # self.available_cards.update([_ for _ in card.daughters])
        self.available_cards.update(card.daughters)
        self.last_card = card.id_card

        card.show_card()
