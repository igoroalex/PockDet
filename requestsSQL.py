import json

import psycopg
from psycopg.rows import dict_row

from config import CONNINFO


def db_fetchall(request: str, args_request: dict) -> dict_row:
    conn = psycopg.connect(conninfo=CONNINFO)

    try:
        with conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(request, args_request)
                data_sql = cur.fetchall()
    finally:
        conn.close()
    return data_sql


def db_commit(request: str, args_request: dict):
    conn = psycopg.connect(conninfo=CONNINFO)

    try:
        with conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(request, args_request)
                conn.commit()
    finally:
        conn.close()


def get_data_hand(user_name: str) -> dict_row:

    return db_fetchall(
        "SELECT * FROM hands WHERE user_name = %(user_name)s;", {"user_name": user_name}
    )


def save_db(hand):
    db_commit(
        """INSERT INTO hands VALUES (%(user_name)s, 
                                                    %(opened_cards)s, 
                                                    %(available_cards)s, 
                                                    %(time_left)s, 
                                                    %(police)s, 
                                                    %(police_cards)s, 
                                                    %(last_card)s, 
                                                    %(jail)s, 
                                                    %(rate)s);""",
        {
            "user_name": hand.user_name,
            "opened_cards": json.dumps(list(hand.opened_cards)),
            "available_cards": json.dumps(list(hand.available_cards)),
            "time_left": hand.time_left,
            "police": hand.police,
            "police_cards": json.dumps(list(hand.police_cards)),
            "last_card": hand.last_card,
            "jail": hand.jail,
            "rate": hand.rate,
        },
    )


def update_db(hand):
    db_commit(
        """UPDATE hands SET user_name = %(user_name)s, 
                                opened_cards = %(opened_cards)s, 
                                available_cards = %(available_cards)s, 
                                time_left = %(time_left)s, 
                                police = %(police)s, 
                                police_cards = %(police_cards)s, 
                                last_card = %(last_card)s, 
                                jail = %(jail)s, 
                                rate = %(rate)s
                            WHERE user_name = %(user_name)s;""",
        {
            "user_name": hand.user_name,
            "opened_cards": json.dumps(list(hand.opened_cards)),
            "available_cards": json.dumps(list(hand.available_cards)),
            "time_left": hand.time_left,
            "police": hand.police,
            "police_cards": json.dumps(list(hand.police_cards)),
            "last_card": hand.last_card,
            "jail": hand.jail,
            "rate": hand.rate,
        },
    )


def save_hand(hand):

    data_sql = get_data_hand(hand.user_name)
    save_db(hand) if not data_sql else update_db(hand)
