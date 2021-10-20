from hand import get_hand


class User:
    def __init__(self, id_t: str):
        self.id: str = id_t


if __name__ == "__main__":

    user_name = "goro2"
    current_user = User(user_name)

    while 1:

        hand = get_hand(user_name)

        print(hand)

        wanted_card = input("wanted card:").lower()
        if wanted_card == "exit":
            break

        hand.want_card(wanted_card)
