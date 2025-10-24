import json
import logging
from typing import Any
import urllib.request

from hexdump import hexdump

from google.protobuf.internal.decoder import _DecodeVarint32
from messages_pb2 import GuildPlayerHeader
from mitmproxy import tcp

CLASS_MAP = {
    1: "swordbearer",
    2: "wayfarer",
    3: "scholar",
    4: "shadowlash",
    5: "acolyte"
}

def parse_character_info(message: bytes) -> GuildPlayerHeader:
    if message.find(bytes.fromhex("0c0f000000")) == -1:
        raise Exception("Cannot parse character info: command signature not found")

    logging.info("Player header message detected!")
    player = GuildPlayerHeader()
    payload_start = (
        message.find(bytes.fromhex("0c0f000000")) + 11
    )  # Skip the length prefix
    payload = message[payload_start:]
    length, pos = _DecodeVarint32(payload, 0)
    message_data = payload[pos : pos + length]
    logging.info(hexdump(message_data))
    player.ParseFromString(message_data)
    send_payload: dict[str, Any] = {"players": []}
    guildName = "no guild"
    if player.guildName is not None and player.guildName != "":
        guildName = player.guildName
    send_payload["players"].append(
        {
            "id": player.id,
            "nickname": player.name,
            "lvl": player.lvl,
            "cls": CLASS_MAP[player.player_class // 1000],
            "stage": player.stage,
            "power": player.power,
            "guild": guildName
        }
    )
    logging.info(
        f"Player Name: {player.name}, Guild: {guildName}, Level: {player.lvl}, Class: {CLASS_MAP[player.player_class // 1000]}, Stage: {player.stage}, Power: {player.power}"
    )
    _ = post_json(
        "http://stream1.transcriptic.ru:5997/v1/players/add",
        payload=send_payload,
    )

    return player

def post_json(url, payload, headers=None):
    data = json.dumps(payload).encode()
    hdrs = {"Content-Type": "application/json"}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, data=data, headers=hdrs, method="POST")
    with urllib.request.urlopen(req):
        return


class SimpleTCPInterceptor:
    def tcp_start(self, flow: tcp.TCPFlow):
        """A TCP connection has started."""
        logging.info(
            f"TCP connection started: {flow.client_conn.peername} -> {flow.server_conn.peername}"
        )

    def tcp_message(self, flow: tcp.TCPFlow):
        if flow.server_conn.address and flow.server_conn.address[1] == 9190:
            message = flow.messages[-1]  # Get the most recent message
            if message.content.find(bytes.fromhex("0c0f000000")) != -1:
                parse_character_info(message.content)

    def tcp_end(self, flow: tcp.TCPFlow):
        """A TCP connection has ended."""
        logging.info(
            f"TCP connection ended: {flow.client_conn.peername} -> {flow.server_conn.peername}"
        )

    def tcp_error(self, flow: tcp.TCPFlow):
        """A TCP error has occurred."""
        logging.info(f"TCP error: {flow.error}")


addons = [SimpleTCPInterceptor()]
