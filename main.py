from teleAPI import start_tele_bot


class User:
    def __init__(self, user_name: str):
        self.user_name: str = user_name


if __name__ == "__main__":

    start_tele_bot()

