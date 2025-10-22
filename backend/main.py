import logging

from flask import Flask, Response, request
from prometheus_client import CONTENT_TYPE_LATEST, Gauge, generate_latest

player_power = Gauge("player_power", "Player power", ["player_id"])
player_lvl = Gauge("player_lvl", "Player level", ["player_id"])
player_stage = Gauge("player_stage", "Player stage", ["player_id"])

# info metric: holds nickname as label (value is constant 1)
player_info = Gauge(
    "player_info",
    "Player info (label values contain nickname)",
    ["player_id", "nickname"],
)

# in-memory map to know previous nickname for a player so we can remove old label combos
_player_nick_map: dict[str, str] = {}  # { str(player_id): "sanitized_nickname" }

# player_dragon_dmg = Gauge("magav2_player_dragon_dmg", "Player dragon damage", ["player_id"])

logger = logging.getLogger("pylogger")

logger.setLevel(logging.DEBUG)

logger.info("starting server...")

app = Flask("gogostats")


def sanitize_label_value(s, max_len=100):
    """Make nickname safe as a label value: trim, replace problematic characters."""
    if s is None:
        return ""
    # convert to str, strip whitespace
    v = str(s).strip()
    # replace characters that may complicate queries or rendering
    for ch in ['"', "'", "\\", "}", "{", "\n", "\r", "\t"]:
        v = v.replace(ch, "_")
    # optionally collapse multiple spaces
    v = " ".join(v.split())
    # trim
    if len(v) > max_len:
        v = v[:max_len]
    return v


def set_player_metrics(
    player_id: int,
    nickname: str | None = None,
    power: int | None = None,
    lvl: int | None = None,
    stage: int | None = None,
    dragon_dmg: int | None = None,
):
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

    # if dragon_dmg is not None:
    # player_dragon_dmg.labels(player_id=pid).set(dragon_dmg)


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.route("/v1/players/add", methods=["POST"])
def flask_players_add():
    logger.info("flask request", extra={"tags": {"url": request.url}})
    req = request.get_json()
    print(req)

    players = req["players"]

    for player in players:
        nickname = player["nickname"]
        id = player["id"]
        lvl = player["lvl"]
        # cls = player["cls"]
        stage = player["stage"]
        power = player["power"]

        set_player_metrics(id, nickname, power, lvl, stage)

    return "", 200


if __name__ == "__main__":
    app.run("0.0.0.0", port=5997, debug=True)
