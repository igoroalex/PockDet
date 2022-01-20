class Answers:
    def __init__(self, reply=None):
        self.replies: list = [reply] if reply else list()

    def add_answer(self, answer):
        if isinstance(answer, list):
            self.replies.extend(answer)
        else:
            self.replies.append(answer)

    def get_answers(self):
        return self.replies


class Answer:
    def __init__(self, body: str):
        self.body = body

    def is_text(self):
        return False

    def is_picture(self):
        return False

    def is_button(self):
        return False


class AnswerText(Answer):
    def is_text(self):
        return True


class AnswerPicture(Answer):
    def is_picture(self):
        return True


class AnswerButton(Answer):
    def is_button(self):
        return True
