Все совпадения случайны.
Это не комерческий, не прибыльный, не социальный проект.
Проект создан для тренировки, практики и своего удовльствия.
Не делиться этим проектом без соглашения интелектуального собственника.
Участие в проекте - это согласие с условиями проекта без притензий.

+++ GoRa +++

PockDect - карточная настольная игра-детектив, гже нужно раскрыть престпления открывая карты и находя улики и информацию.
Изначально игра построена на команду из нескольких человек, но в данном случае это соло игра, так что по контексту принимает это во внимание.
После старта игры, правила описываются в первых картах. Продвинуться дальше в расследовании просто ввести название карты латиницей (например: s3, f1).

used Python 3.9, psycopg (https://www.psycopg.org/psycopg3/docs/basic/install.html), PostgreSQL (https://www.postgresql.org/download/)

example config.py:

CONNINFO: str = "postgresql://user_1:XXXXXXX@localhost:5432/test1"

TOKEN: str = "XXXXXXXXXXX:XXXXXXXXXXXXXXXXXXXX"

LINK: str = "t.me/QuarantinedDetectiveBot"

# TODOs:
 - environment variables
 - pictures links on webserver
 - made Docker
