from hand import Hand


class User:
    def __init__(self, user_name: str):
        self.user_name: str = user_name


if __name__ == "__main__":

    current_user = User(input("your name:"))

    while 1:

        hand = Hand.get_hand(current_user.user_name)

        print(hand)

        wanted_card = input("wanted card:").lower()
        if wanted_card == "exit":
            break

        hand.want_card(wanted_card)
