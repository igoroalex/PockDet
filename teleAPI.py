from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import TOKEN
from hand import Hand, DECK
from requestsSQL import delete_hand


class Answer:
    def __init__(self, picture: str = "", notice: str = ""):
        self.pictures: list = [picture] if picture else []
        self.notice: str = notice


def start(update, context):
    with open("greetings.txt", "r") as f:
        greetings = f.read()

    reply_text(update, greetings)
    reply_text(update, "/start_game")


def id_user(chat):
    return chat.username if chat.username else str(chat.id)


def help_game(update, context):
    hand = Hand.get_hand(id_user(update.message.chat))
    reply_text(
        update, f"/next_cards - доступные НЕ открытые карты: {hand.next_cards()}"
    )
    reply_text(update, f"/time_left - прошло время: {hand.time_left}")
    reply_text(update, f"/m1 - закончить расследование")


def error(update, context):
    reply_text(update, "an error occurred")


def unknown(update, context):
    reply_text(update, "Извини, я очень ограничен в ответах)))")


def my_user_name(update, context):
    reply_text(update, id_user(update.message.chat))


def start_game(update, context):
    reply_text(update, "Начнем расследование")

    hand = Hand.get_hand(id_user(update.message.chat))
    show_answer(update, hand.answer(DECK.start_investigation()))


def finish_investigation(update, context):
    hand = Hand.get_hand(id_user(update.message.chat))
    show_answer(update, hand.answer(DECK.finish_investigation()))


def restart(update, context):
    hand = Hand.get_hand(id_user(update.message.chat))
    delete_hand(hand)

    start(update, context)


def time_left(update, context):
    hand = Hand.get_hand(id_user(update.message.chat))
    reply_text(update, f"прошло время: {hand.time_left}")


def next_cards(update, context):
    hand = Hand.get_hand(id_user(update.message.chat))
    reply_text(update, f"доступные НЕ открытые карты: {hand.next_cards()}")


def text(update, context):
    hand = Hand.get_hand(id_user(update.message.chat))
    show_answer(update, hand.answer(update.message.text))


def show_picture(update, answer: Answer):
    for picture in answer.pictures:
        update.message.reply_photo(open(picture, "rb"))


def show_notice(update, answer: Answer):
    if answer.notice:
        reply_text(update, answer.notice)


def show_answer(update, answer: Answer):
    show_picture(update, answer)
    show_notice(update, answer)


def reply_text(update, text_answer: str):
    update.message.reply_text(text_answer)


def command_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_game))
    dispatcher.add_handler(CommandHandler("start_game", start_game))
    dispatcher.add_handler(CommandHandler("zero_hand", restart))
    dispatcher.add_handler(CommandHandler("next_cards", next_cards))
    dispatcher.add_handler(CommandHandler("time_left", time_left))
    dispatcher.add_handler(CommandHandler("my_user_name", my_user_name))
    dispatcher.add_handler(CommandHandler("m1", finish_investigation))

    dispatcher.add_handler(MessageHandler(Filters.text, text))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))


def start_tele_bot():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    command_handlers(dispatcher)
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()
