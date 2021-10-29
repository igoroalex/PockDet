from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import TOKEN
from hand import Hand, Answer


def start(update, context):
    with open("greetings.txt", "r") as f:
        greetings = f.read()

    update.message.reply_text(greetings)
    update.message.reply_text("/start_game")


def help_game(update, context):

    hand = Hand.get_hand(update.message.chat.username)

    update.message.reply_text(f"your next cards: {hand.next_cards()}")


def error(update, context):
    update.message.reply_text("an error occured")


def unknown(update, context):
    update.message.reply_text("Sorry, I didn't understand that command.")


def start_game(update, context):

    update.message.reply_text("Lets go")


def text(update, context):

    # RegExp

    hand: Hand = Hand.get_hand(update.message.chat.username)

    answer: Answer = hand.answer(update.message.text)

    show_notice(update, answer) if answer.notice else show_picture(update, answer)


def show_picture(update, answer: Answer):
    for picture in answer.pictures:
        update.message.reply_photo(open(picture, 'rb'))


def show_notice(update, answer: Answer):
    update.message.reply_text(answer.notice)


def start_tele_bot():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_game))
    dispatcher.add_handler(CommandHandler("start_game", start_game))

    dispatcher.add_handler(MessageHandler(Filters.text, text))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()
