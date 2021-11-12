from typing import List, Final
import webbrowser
from deck import Deck


DECK: Final = Deck()


class Answer:
    def __init__(self, picture: str = "", notice: str = ""):
        self.pictures: list = [picture] if picture else []
        self.notice: str = notice


class Card:
    def __init__(self, id_card: str):
        data_card = DECK.all_cards.get(id_card, {})

        self.id_card: str = data_card.get("id_card", "")
        self.time: int = data_card.get("time", 0)
        self.daughters: List[str] = data_card.get("daughters", [])
        self.next_card: str = data_card.get("next_card", "")
        self.police: int = data_card.get("police", 0)
        self.answer: Answer = Answer()

    def __str__(self):
        return f"{self.id_card=}, {self.time=}, {self.daughters=}, {self.next_card=}"

    @staticmethod
    def get_card(id_card: str):
        special_cards = {
            "s3": CardS3,
            "s4": CardS4,
            "c9": CardC9,
            "h2": CardH2,
            "f4": CardF4,
            "e2": CardE2,
            "p5": CardP5,
            "p6": CardP6,
            "m2": CardM2,
            "m4": CardM4,
            "m5": CardM5,
            "m6": CardM6,
            "m7": CardM7,
            "m8": CardM8,
            "m9": CardM9,
            "m10": CardM10,
            "p10": CardP10,
        }
        return special_cards.get(id_card, Card)(id_card)

    def show_card(self):
        webbrowser.open(rf"dangerous_ties/{self.id_card}.jpg")

    def picture(self):
        return rf"dangerous_ties/{self.id_card}.jpg"

    def check(self, hand) -> bool:
        return True


class CardS3(Card):
    def check(self, hand) -> bool:
        if hand.time_left > 2:
            self.answer = Answer(
                notice="Момент упущен. Полиция уже приехала и не допускает посторонних людей"
            )
            return False
        return True


class CardS4(Card):
    def check(self, hand) -> bool:
        if hand.time_left > 5:
            self.answer = Answer(notice="Соседи разошлись. не успели(((")
            self.daughters = []
            return False
        return True


class CardC9(Card):
    def check(self, hand) -> bool:
        if hand.last_card != "c8":
            self.answer = Answer(
                notice="Возможность подслушать упущена. Не стоило видимо уходить"
            )
            return False
        return True


class CardH2(Card):
    def check(self, hand) -> bool:
        if hand.time_left <= 4:
            self.police = 0
        return True


class CardF4(Card):
    def check(self, hand) -> bool:
        if (14 <= hand.time_left <= 22) or (38 <= hand.time_left <= 46):
            self.next_card = "f6"
            hand.available_cards.add(self.next_card)
        return True


class CardE2(Card):
    def check(self, hand) -> bool:
        if "h6" in hand.opened_cards:
            self.police = 0
            self.next_card = "e3"
            hand.available_cards.add(self.next_card)
        return True


class CardP5(Card):
    def check(self, hand) -> bool:
        hand.jail = "p5"
        hand.available_cards = {
            _ for _ in hand.available_cards if not _.startswith("c")
        }
        return True


class CardP6(Card):
    def check(self, hand) -> bool:
        hand.jail = "p6"
        self.next_card = "m1"
        hand.available_cards = {self.next_card}
        self.daughters.append(self.next_card)
        return True


class CardM2(Card):
    def check(self, hand) -> bool:
        if hand.jail == "p6":
            hand.rate += 5
            self.next_card = "m10"
            self.daughters.append(self.next_card)
        return True


class CardM4(Card):
    def check(self, hand) -> bool:
        if hand.jail == "p6":
            hand.rate += 7
            self.next_card = "m10"
            self.daughters.append(self.next_card)
        return True


class CardM5(Card):
    def check(self, hand) -> bool:
        if hand.jail == "p6":
            hand.rate += 15
            self.next_card = "m10"
            self.daughters.append(self.next_card)
        return True


class CardM6(Card):
    def check(self, hand) -> bool:
        if hand.jail == "p6":
            hand.rate += 9
            self.next_card = "m10"
            self.daughters.append(self.next_card)
        return True


class CardM7(Card):
    def check(self, hand) -> bool:
        hand.rate += 100
        hand.rate -= sum(
            [20 for _ in hand.opened_cards if _ in ("m2", "m4", "m5", "m6", "m8", "m9")]
        )
        hand.rate -= hand.time_left
        hand.rate -= 10 if hand.jail == "p6" else 0
        # self.next_card = "m10"
        # self.daughters.append(self.next_card)
        return True


class CardM8(Card):
    def check(self, hand) -> bool:
        if hand.jail == "p6":
            hand.rate += 65
            hand.rate -= sum(
                [
                    20
                    for _ in hand.opened_cards
                    if _.startswith("m") and _ not in ("m1", "m3", "m8")
                ]
            )
            hand.rate -= hand.time_left
            # self.next_card = "m10"
            # self.daughters.append(self.next_card)
        return True


class CardM9(Card):
    def check(self, hand) -> bool:
        if hand.jail == "p6":
            hand.rate += 70
            hand.rate -= sum(
                [
                    20
                    for _ in hand.opened_cards
                    if _.startswith("m") and _ not in ("m1", "m3", "m9")
                ]
            )
            hand.rate -= hand.time_left
            # self.next_card = "m10"
            # self.daughters.append(self.next_card)
        return True


class CardM10(Card):
    def check(self, hand) -> bool:
        self.answer = Answer(notice=f"Ваш результат: {hand.rate}")
        return True


class CardP10(Card):
    def check(self, hand) -> bool:
        self.answer = Answer(notice="!!!Поздравляю!!!")
        return True
