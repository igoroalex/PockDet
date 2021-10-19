import psycopg
from psycopg.rows import dict_row

conn = psycopg.connect(conninfo="postgresql://postgres:789456@localhost:5432/test1")
cur = conn.cursor()

# cur.execute(
#     """INSERT INTO hands (user_name, time_left) VALUES (%(user_name)s, %(time_left)s);""",
#     {"user_name": "len", "time_left": 15},
# )
# conn.commit()

cur.execute("SELECT * FROM hands")

full_fetch = cur.fetchall()
for item in full_fetch:
    print(f"{item=} {type(item)=}")

cur.close()
conn.close()

with psycopg.connect(
    conninfo="postgresql://postgres:789456@localhost:5432/test1"
) as conn:
    with conn.cursor(row_factory=dict_row) as cur:

        cur.execute("SELECT * FROM hands")
        full_fetch = cur.fetchall()
        print(full_fetch)

conn = psycopg.connect(conninfo="postgresql://postgres:789456@localhost:5432/test1")
try:
    with conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute("SELECT * FROM hands")
            full_fetch = cur.fetchall()
            print(full_fetch)
finally:
    conn.close()

with conn:
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT * FROM hands")
        full_fetch = cur.fetchall()
        print(full_fetch)
