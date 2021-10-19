from hand import Hand


class User:
    def __init__(self, id_t: str):
        self.id: str = id_t


if __name__ == "__main__":

    user_name = "goro"
    current_user = User(user_name)

    wanted_card = "i1"
    hand = Hand(wanted_card)

    while True:
        hand.want_card(wanted_card)

        print(hand)

        wanted_card = input("wanted card:").lower()
        if wanted_card == "exit":
            break
