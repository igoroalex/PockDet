import json
from typing import Set, List

from card import Card
from deck import DECK
from teleanswer import Answers, AnswerText
from requestsSQL import get_data_hand, save_hand


class Hand:
    """Hand - player's data in game"""

    def __init__(self, pattern_hand: dict):

        self.user_name: str = pattern_hand["user_name"]
        self.opened_cards: Set[str] = pattern_hand["opened_cards"]
        self.available_cards: Set[str] = pattern_hand["available_cards"]
        self.time_left: int = pattern_hand["time_left"]
        self.police: int = pattern_hand["police"]
        self.police_cards: List[str] = pattern_hand["police_cards"]
        self.last_card: str = pattern_hand["last_card"]
        self.jail: str = pattern_hand["jail"]
        self.rate: int = pattern_hand["rate"]

    def __str__(self):
        return (
            f"{self.time_left=}, "
            f"{self.police=}, "
            f"{self.police_cards}, "
            f"{self.last_card}, "
            f"{self.jail}, "
            f"{self.available_cards}"
        )

    @classmethod
    def get_hand(cls, user_name: str):
        data_sql = get_data_hand(user_name)
        return (
            cls.old_hand(user_name, data_sql[0])
            if data_sql
            else cls.zero_hand(user_name)
        )

    @staticmethod
    def zero_hand(user_name: str):
        pattern_hand = {
            "user_name": user_name,
            "opened_cards": set(),
            "available_cards": {DECK.start_investigation()},
            "time_left": 0,
            "police": 0,
            "police_cards": DECK.police_cards(),
            "last_card": "",
            "jail": "",
            "rate": 0,
        }

        return Hand(pattern_hand)

    @staticmethod
    def old_hand(user_name: str, data_user: dict):

        pattern_hand = {
            "user_name": user_name,
            "opened_cards": set(json.loads(data_user["opened_cards"])),
            "available_cards": set(json.loads(data_user["available_cards"])),
            "time_left": data_user["time_left"],
            "police": data_user["police"],
            "police_cards": json.loads(data_user["police_cards"]),
            "last_card": data_user["last_card"],
            "jail": data_user["jail"],
            "rate": data_user["rate"],
        }

        return Hand(pattern_hand)

    def next_cards(self) -> set:
        return self.available_cards.difference(self.opened_cards)

    def answer(self, id_card: str):

        id_card = id_card.lower().strip()

        answers = Answers()

        if not self.available(id_card):
            answers.add_answer(
                AnswerText(
                    f"Карта {id_card} не доступна. Эти карты Вы еще не открывали {self.next_cards()}"
                )
            )
            return answers

        card = Card.get_card(id_card)

        if self.show_opened(card):
            answers.add_answer(card.answer(self))
            return answers

        if card.help_police(self):
            answers.add_answer(
                AnswerText(f"Вы не можете пользоваться помощью друзей в полиции")
            )
            return answers

        if not card.check(self):
            answers.add_answer(card.notice())
            return answers

        self.police_noticed(card)

        self.play(card, answers)

        card.check_jail(self)

        return answers

    def show_opened(self, card: Card) -> bool:
        return card.id_card in self.opened_cards

    def available(self, id_card: str) -> bool:
        return id_card in self.available_cards

    def police_noticed(self, card: Card):
        if card.police:
            card.next_card = self.police_cards.pop()
            self.available_cards.add(card.next_card)

    def play(self, card: Card, answers):

        card.check_jail(self)

        self.time_left += card.time
        self.police += card.police
        self.opened_cards.add(card.id_card)
        self.available_cards.update(card.daughters)
        self.last_card = card.id_card

        save_hand(self)

        answers.add_answer(card.answer(self))

        if card.next_card:
            self.play(Card.get_card(card.next_card), answers)

    def find_parent(self, id_card: str):
        id_card = id_card.lower().strip()

        for id_parent in self.available_cards:
            data_parent = DECK.all_cards.get(id_parent, {})

            if id_card in data_parent.get("daughters", []):
                return self.answer(data_parent.get("id_card", ""))

        return self.answer(id_card)
