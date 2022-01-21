import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
)
from config import TOKEN
from deck import DECK
from hand import Hand
from requestsSQL import delete_hand
from teleanswer import Answers, AnswerText

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()


def start_tele_bot():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    set_handlers(dispatcher)
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


def set_handlers(dispatcher):
    command_handlers = {
        "start": start,
        "help": help_game,
        "start_game": start_game,
        "zero_hand": restart,
        "next_cards": next_cards,
        "time_left": time_left,
        "my_user_name": my_user_name,
        "find_parent": find_parent,
        "m1": finish_investigation,
    }
    add_handlers(dispatcher, command_handlers)

    dispatcher.add_handler(MessageHandler(Filters.text, text))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    dispatcher.add_handler(CallbackQueryHandler(button))


def add_handlers(dispatcher, command_handlers):
    for command, callback in command_handlers.items():
        dispatcher.add_handler(CommandHandler(command, callback))


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
            AnswerText(f"/find_parent xx - найти карту, которая привела к карте хх"),
            AnswerText(f"/m1 - закончить расследование"),
        ]
    )

    show_answers(update, answers)
    show_buttons(update)


def next_cards(update, context):
    hand = Hand.get_hand(id_user(update.message.chat))
    show_answers(
        update, Answers(AnswerText(f"доступные НЕ открытые карты: {hand.next_cards()}"))
    )
    print(update.message.text)


def find_parent(update, context):
    """find the card that led to the desired"""
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
        elif answer.is_button():
            reply_text(update, answer.body)
        elif answer.is_text():
            reply_text(update, answer.body)


def reply_text(update, text_answer: str):
    update.message.reply_text(text_answer)


def reply_picture(update, picture_answer: str):
    update.message.reply_photo(open(picture_answer, "rb"))


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i : i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def show_buttons(update):
    # список кнопок
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data="1"),
            InlineKeyboardButton("Option 2", callback_data="2"),
        ],
        [InlineKeyboardButton("Option 3", callback_data="3")],
    ]

    # сборка клавиатуры из кнопок `InlineKeyboardButton`
    # reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=2))
    reply_markup = InlineKeyboardMarkup(keyboard)
    # отправка клавиатуры в чат
    update.message.reply_text("Пожалуйста, выберите:", reply_markup=reply_markup)


def button(update, _):
    query = update.callback_query
    variant = query.data
    query.answer()
    # query.edit_message_text(text=f"s1")
    query.edit_message_text(text=f"{str(query)}")
