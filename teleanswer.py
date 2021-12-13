class Answers:
    def __init__(self):
        self.replies: list = list()

    def add_answer(self, reply):
        self.replies.append(reply)

    def get_answers(self):
        return self.replies


class Answer:
    # def __init__(self, picture: str = "", message: str = ""):
    #     self.pictures: list = [picture] if picture else []
    #     self.message: str = message

    def type_message(self):
        raise NotImplementedError

    def is_text(self):
        return False

    def is_picture(self):
        return False


class AnswerText(Answer):
    def __init__(self, body: str):
        self.body = body

    def type_message(self):
        return "text"

    def is_text(self):
        return True


class AnswerPicture(Answer):
    def __init__(self, body: str):
        self.body = body

    def type_message(self):
        return "picture"

    def is_picture(self):
        return True
