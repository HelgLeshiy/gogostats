import logging
from typing import Any

from flask import Flask, Response, request
from prometheus_client import CONTENT_TYPE_LATEST, Gauge, generate_latest


class PlayerMetrics:
    def __init__(self) -> None:
        self._common_labels = ["player_id", "nickname", "guild", "class"]

        self._player_power = Gauge("player_power", "Player power", self._common_labels)
        self._player_lvl = Gauge("player_lvl", "Player level", self._common_labels)
        self._player_stage = Gauge(
            "player_stage", "Main story stage", self._common_labels
        )
        self._player_dragon_dmg = Gauge(
            "player_dragon_dmg", "Player dragon damage", self._common_labels
        )

        self._player_cache: dict[int, dict[str, Any]] = {}

    def _get_labels(
        self,
        player_id: int,
        nickname: str | None = None,
        guild: str | None = None,
        player_class: str | None = None,
    ) -> dict[str, Any] | None:
        """Get or create label dictionary for a player"""
        key = player_id
        if key not in self._player_cache:
            if nickname is None or guild is None or player_class is None:
                return None

            self._player_cache[key] = {
                "player_id": player_id,
                "nickname": nickname,
                "guild": guild,
                "class": player_class,
            }
        return self._player_cache[key]

    def update_player_metrics(
        self,
        player_id: int,
        nickname: str,
        guild: str,
        player_class: str,
        power: int,
        level: int,
        stage: int,
    ) -> None:
        labels = self._get_labels(player_id, nickname, guild, player_class)
        if labels is None:
            return

        self._player_power.labels(**labels).set(power)
        self._player_lvl.labels(**labels).set(level)
        self._player_stage.labels(**labels).set(stage)

    def update_player_dragon_dmg(self, player_id: int, dragon_dmg: int) -> None:
        labels = self._get_labels(player_id)
        if labels is None:
            return

        self._player_dragon_dmg.labels(**labels).set(dragon_dmg)


logger = logging.getLogger("pylogger")
logger.setLevel(logging.DEBUG)
logger.info("starting server...")
app = Flask("gogostats")

player_metrics = PlayerMetrics()


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
        cls = player["cls"]
        guild = player["guild"]
        stage = player["stage"]
        power = player["power"]

        player_metrics.update_player_metrics(
            id, nickname, guild, cls, power, lvl, stage
        )

    return "", 200


@app.route("/v1/dragon_damage/add", methods=["POST"])
def flask_dragon_damage_add():
    logger.info("flask request", extra={"tags": {"url": request.url}})
    req = request.get_json()
    print(req)

    players = req["players"]

    for player in players:
        id = player["id"]
        dmg = player["dmg"]
        player_metrics.update_player_dragon_dmg(id, dmg)

    return "", 200


if __name__ == "__main__":
    app.run("0.0.0.0", port=5997, debug=True)
