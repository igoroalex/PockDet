class Answer:
    def __init__(self, picture: str = "", message: str = ""):
        self.pictures: list = [picture] if picture else []
        self.message: str = message