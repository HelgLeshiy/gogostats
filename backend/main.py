from flask import Flask
from flask import request
from flask import jsonify
from flask import Response

import os

import psycopg2
from psycopg2.extras import NamedTupleCursor

import logging
import datetime

from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST

player_power = Gauge("player_power", "Player power", ["player_id"])
player_lvl = Gauge("player_lvl", "Player level", ["player_id"])
player_stage = Gauge("player_stage", "Player stage", ["player_id"])
player_nickname = Gauge("player_nickname", "Player nickname", ["player_id"])

# info metric: holds nickname as label (value is constant 1)
player_info = Gauge("player_info", "Player info (label values contain nickname)", ["player_id", "nickname"])

# in-memory map to know previous nickname for a player so we can remove old label combos
_player_nick_map = {}  # { str(player_id): "sanitized_nickname" }

#player_dragon_dmg = Gauge("magav2_player_dragon_dmg", "Player dragon damage", ["player_id"])

logger = logging.getLogger("pylogger")

logger.setLevel(logging.DEBUG)

logger.info("starting server...")

app = Flask("magav2")

def sanitize_label_value(s, max_len=100):
    """Make nickname safe as a label value: trim, replace problematic characters."""
    if s is None:
        return ""
    # convert to str, strip whitespace
    v = str(s).strip()
    # replace characters that may complicate queries or rendering
    for ch in ['"', "'", '\\', '}', '{', '\n', '\r', '\t']:
        v = v.replace(ch, '_')
    # optionally collapse multiple spaces
    v = " ".join(v.split())
    # trim
    if len(v) > max_len:
        v = v[:max_len]
    return v

def set_player_metrics(player_id, nickname=None, power=None, lvl=None, stage=None, dragon_dmg=None):
    pid = str(player_id)
    if power is not None:
        player_power.labels(player_id=pid).set(power)
    if lvl is not None:
        player_lvl.labels(player_id=pid).set(lvl)
    if stage is not None:
        player_stage.labels(player_id=pid).set(stage)

    if nickname is not None:
        nick_s = sanitize_label_value(nickname)
        prev = _player_nick_map.get(pid)
        # if nickname changed, remove old label pair to avoid stale series
        if prev is not None and prev != nick_s:
            try:
                player_info.remove(player_id=pid, nickname=prev)
            except KeyError:
                pass
        # set new pair
        player_info.labels(player_id=pid, nickname=nick_s).set(1)
        # record current nickname
        _player_nick_map[pid] = nick_s
    #if dragon_dmg is not None:
        #player_dragon_dmg.labels(player_id=pid).set(dragon_dmg)

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route('/v1/players/add', methods=['POST'])
def flask_players_add():
    logger.info("flask request", extra={"tags": {"url": request.url}})
    req = request.get_json()
    print(req)

    players = req["players"]

    for player in players:
        nickname = player["nickname"]
        id = player["id"]
        lvl = player["lvl"]
        #cls = player["cls"]
        stage = player["stage"]
        power = player["power"]

        #now = datetime.datetime.now(datetime.timezone.utc)

        set_player_metrics(id, nickname, power, lvl, stage)

    # conn = psycopg2.connect(dbname='kakebo', user='whisper', password='2whisper2', host='91.105.196.201', port="5000")

    # with conn.cursor() as curs:
    #     curs.execute('INSERT INTO gogo_stats (id, nickname, lvl, class, stage, power, date) VALUES (%s, %s, %s, %s, %s, %s, %s)', (id, nickname, lvl, cls, stage, power, now,))
    # conn.commit()
    # conn.close()

    return "", 200

# @app.route('/v1/players/dmg_add', methods=['POST'])
# def flask_players_dmg_add():
#     logger.info("flask request", extra={"tags": {"url": request.url}})
#     req = request.get_json()
#     print(req)

#     id = req["id"]
#     dmg = req["dmg"]

#     now = datetime.datetime.now(datetime.timezone.utc)

#     conn = psycopg2.connect(dbname='kakebo', user='whisper', password='2whisper2', host='91.105.196.201', port="5000")
#     rowcount = 0
#     with conn.cursor() as curs:
#         curs.execute('UPDATE gogo_stats SET dragon_dmg = %s WHERE id = %s AND date = (SELECT MAX(date) from gogo_stats WHERE id = %s)', (dmg, id, id,))
#         rowcount = curs.rowcount
#     conn.commit()
#     conn.close()

#     return str(rowcount), 200

# @app.route('/v1/players', methods=['GET'])
# def flask_players():
#     logger.info("flask request", extra={"tags": {"url": request.url}})

#     conn = psycopg2.connect(dbname='kakebo', user='whisper', password='2whisper2', host='91.105.196.201', port="5000")
#     players = []
#     with conn.cursor() as curs:
#         curs.execute('''
#                     select t.id, t.nickname, t.lvl, t.class, t.stage, t.power, t.dragon_dmg, t.date
#                     from gogo_stats t
#                     inner join (
#                         select id, max(date) as MaxDate
#                         from gogo_stats
#                         group by id
#                     ) tm on t.id = tm.id and t.date = tm.MaxDate
#                     order by t.power desc
#                     ''')
#         rows = curs.fetchall()
#         for row in rows:
#             players.append({
#                 "id": row[0],
#                 "nickname": row[1],
#                 "lvl": row[2],
#                 "cls": row[3],
#                 "stage": row[4],
#                 "power": row[5],
#                 "dragon_dmg": 0 if row[6] is None else row[6],
#                 "update_date": row[7]
#             })

#     conn.close()

#     return { "players": players }


if __name__ == "__main__":
    app.run('0.0.0.0', port=5997, debug=True)