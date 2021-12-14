from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import TOKEN
from deck import DECK
from hand import Hand
from requestsSQL import delete_hand
from teleanswer import Answers, AnswerText


def start_tele_bot():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    command_handlers(dispatcher)
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


def command_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_game))
    dispatcher.add_handler(CommandHandler("start_game", start_game))
    dispatcher.add_handler(CommandHandler("zero_hand", restart))
    dispatcher.add_handler(CommandHandler("next_cards", next_cards))
    dispatcher.add_handler(CommandHandler("time_left", time_left))
    dispatcher.add_handler(CommandHandler("my_user_name", my_user_name))
    dispatcher.add_handler(CommandHandler("find_parent", find_parent))
    dispatcher.add_handler(CommandHandler("m1", finish_investigation))

    dispatcher.add_handler(MessageHandler(Filters.text, text))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))


def start(update, context):
    with open("greetings.txt", "r") as f:
        greetings = f.read()

    answers = Answers()
    answers.add_answer([AnswerText(greetings), AnswerText("/start_game")])

    show_answers(update, answers)


def start_game(update, context):
    show_answers(update, Answers(AnswerText("Начнем расследование")))

    hand = Hand.get_hand(id_user(update.message.chat))
    show_answers(update, hand.answer(DECK.start_investigation()))


def restart(update, context):
    hand = Hand.get_hand(id_user(update.message.chat))
    delete_hand(hand)

    start(update, context)


def help_game(update, context):
    hand = Hand.get_hand(id_user(update.message.chat))

    answers = Answers()
    answers.add_answer(
        [
            AnswerText(
                f"/next_cards - доступные НЕ открытые карты: {hand.next_cards()}"
            ),
            AnswerText(f"/time_left - прошло время: {hand.time_left}"),
            AnswerText(f"/m1 - закончить расследование"),
        ]
    )

    show_answers(update, answers)


def next_cards(update, context):
    hand = Hand.get_hand(id_user(update.message.chat))
    show_answers(
        update, Answers(AnswerText(f"доступные НЕ открытые карты: {hand.next_cards()}"))
    )
    print(update.message.text)


def find_parent(update, context):
    hand = Hand.get_hand(id_user(update.message.chat))
    id_card = update.message.text.replace("/find_parent", "")
    show_answers(update, hand.find_parent(id_card))


def finish_investigation(update, context):
    hand = Hand.get_hand(id_user(update.message.chat))
    show_answers(update, hand.answer(DECK.finish_investigation()))


def error(update, context):
    show_answers(update, Answers(AnswerText("an error occurred")))


def unknown(update, context):
    show_answers(update, Answers(AnswerText("Извини, я очень ограничен в ответах)))")))


def text(update, context):
    hand = Hand.get_hand(id_user(update.message.chat))
    show_answers(update, hand.answer(update.message.text))


def time_left(update, context):
    hand = Hand.get_hand(id_user(update.message.chat))
    show_answers(update, Answers(AnswerText(f"прошло время: {hand.time_left}")))


def my_user_name(update, context):
    show_answers(update, Answers(AnswerText(id_user(update.message.chat))))


def id_user(chat):
    return chat.username if chat.username else str(chat.id)


def show_answers(update, answers):
    for answer in answers.get_answers():
        if answer.is_picture():
            reply_picture(update, answer.body)
        elif answer.is_text():
            reply_text(update, answer.body)


def reply_text(update, text_answer: str):
    update.message.reply_text(text_answer)


def reply_picture(update, picture_answer: str):
    update.message.reply_photo(open(picture_answer, "rb"))
