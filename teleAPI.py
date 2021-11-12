from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import TOKEN
from hand import Hand, Answer, DECK
from requestsSQL import delete_hand


def start(update, context):
    with open("greetings.txt", "r") as f:
        greetings = f.read()

    update.message.reply_text(greetings)
    update.message.reply_text("/start_game")


def id_user(chat):
    return chat.username if chat.username else str(chat.id)


def help_game(update, context):

    hand = Hand.get_hand(id_user(update.message.chat))
    update.message.reply_text(f"your next cards: {hand.next_cards()}")


def error(update, context):
    update.message.reply_text("an error occured")


def unknown(update, context):
    update.message.reply_text("Sorry, I didn't understand that command.")


def my_user_name(update, context):
    update.message.reply_text(id_user(update.message.chat))


def start_game(update, context):

    update.message.reply_text("Начнем расследование")

    hand: Hand = Hand.get_hand(id_user(update.message.chat))

    # answer: Answer = hand.answer("i1")

    # show_notice(update, answer) if answer.notice else show_picture(update, answer)
    show_answer(update, hand.answer(DECK.first_card()))


def restart(update, context):

    hand: Hand = Hand.get_hand(id_user(update.message.chat))
    delete_hand(hand)

    start(update, context)


def time_left(update, context):

    hand: Hand = Hand.get_hand(id_user(update.message.chat))
    update.message.reply_text(f"прошло время: {hand.time_left}")


def next_cards(update, context):

    hand: Hand = Hand.get_hand(id_user(update.message.chat))
    update.message.reply_text(f"your next cards: {hand.next_cards()}")


def text(update, context):

    # RegExp

    hand: Hand = Hand.get_hand(id_user(update.message.chat))

    answer: Answer = hand.answer(update.message.text)

    show_answer(update, answer)


def show_picture(update, answer: Answer):
    for picture in answer.pictures:
        update.message.reply_photo(open(picture, "rb"))


def show_notice(update, answer: Answer):
    if answer.notice:
        update.message.reply_text(answer.notice)


def show_answer(update, answer: Answer):
    show_picture(update, answer)
    show_notice(update, answer)


def start_tele_bot():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_game))
    dispatcher.add_handler(CommandHandler("start_game", start_game))
    dispatcher.add_handler(CommandHandler("zero_hand", restart))
    dispatcher.add_handler(CommandHandler("next_cards", next_cards))
    dispatcher.add_handler(CommandHandler("time_left", time_left))
    dispatcher.add_handler(CommandHandler("my_user_name", my_user_name))

    dispatcher.add_handler(MessageHandler(Filters.text, text))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()
