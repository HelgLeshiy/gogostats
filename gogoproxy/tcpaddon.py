import json
import logging
import urllib.request

from google.protobuf.internal.decoder import _DecodeVarint32
from messages_pb2 import GuildInfo, GuildMemberList, GuildPlayerHeader
from mitmproxy import tcp


def post_json(url, payload, headers=None):
    data = json.dumps(payload).encode()
    hdrs = {"Content-Type": "application/json"}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, data=data, headers=hdrs, method="POST")
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


class SimpleTCPInterceptor:
    def tcp_start(self, flow: tcp.TCPFlow):
        """A TCP connection has started."""
        logging.info(
            f"TCP connection started: {flow.client_conn.peername} -> {flow.server_conn.peername}"
        )

    def tcp_message(self, flow: tcp.TCPFlow):
        if flow.server_conn.address and flow.server_conn.address[1] == 9190:
            message = flow.messages[-1]  # Get the most recent message
            if message.content.find(bytes.fromhex("1c020000000100000000")) != -1:
                logging.info("GuildInfo message detected!")
                guild_info = GuildInfo()
                payload_start = (
                    message.content.find(bytes.fromhex("1c020000000100000000")) + 13
                )  # Skip the length prefix
                payload = message.content[payload_start:]
                guild_info.ParseFromString(payload)
                payload = {"players": []}
                for member in guild_info.list.guildPlayers:
                    payload["players"].append(
                        {
                            "id": member.header.id,
                            "nickname": member.header.name,
                            "lvl": member.header.lvl,
                            "cls": member.header.player_class,
                            "stage": member.stage,
                            "power": member.power,
                        }
                    )
                    logging.info(
                        f"Player Name: {member.header.name}, Level: {member.header.lvl}, Class: {member.header.player_class}, Stage: {member.stage}, Power: {member.power}"
                    )
                _ = post_json(
                    "http://stream1.transcriptic.ru:5997/v1/players/add",
                    payload=payload,
                )

            if message.content.find(bytes.fromhex("1c030000000100000000")) != -1:
                logging.info("GuildMemberList message detected!")
                guild_member_list = GuildMemberList()
                payload_start = (
                    message.content.find(bytes.fromhex("1c030000000100000000")) + 13
                )  # Skip the length prefix
                payload = message.content[payload_start:]
                guild_member_list.ParseFromString(payload)
                payload = {"players": []}
                for member in guild_member_list.guildPlayers:
                    payload["players"].append(
                        {
                            "id": member.header.id,
                            "nickname": member.header.name,
                            "lvl": member.header.lvl,
                            "cls": member.header.player_class,
                            "stage": member.stage,
                            "power": member.power,
                        }
                    )
                    logging.info(
                        f"Player Name: {member.header.name}, Level: {member.header.lvl}, Class: {member.header.player_class}, Stage: {member.stage}, Power: {member.power}"
                    )
                _ = post_json(
                    "http://stream1.transcriptic.ru:5997/v1/players/add",
                    payload=payload,
                )

            if message.content.find(bytes.fromhex("0c0f0000000100000000")) != -1:
                logging.info("Player header message detected!")
                player = GuildPlayerHeader()
                payload_start = (
                    message.content.find(bytes.fromhex("0c0f0000000100000000")) + 11
                )  # Skip the length prefix
                payload = message.content[payload_start:]
                length, pos = _DecodeVarint32(payload, 0)
                message_data = payload[pos : pos + length]
                player.ParseFromString(message_data)
                send_payload = {"players": []}
                send_payload["players"].append(
                    {
                        "id": player.id,
                        "nickname": player.name,
                        "lvl": player.lvl,
                        "cls": player.player_class,
                        "stage": player.stage,
                        "power": player.power,
                    }
                )
                logging.info(
                    f"Player Name: {player.name}, Level: {player.lvl}, Class: {player.player_class}, Stage: {player.stage}, Power: {player.power}"
                )
                _ = post_json(
                    "http://stream1.transcriptic.ru:5997/v1/players/add",
                    payload=send_payload,
                )

    def tcp_end(self, flow: tcp.TCPFlow):
        """A TCP connection has ended."""
        logging.info(
            f"TCP connection ended: {flow.client_conn.peername} -> {flow.server_conn.peername}"
        )

    def tcp_error(self, flow: tcp.TCPFlow):
        """A TCP error has occurred."""
        logging.info(f"TCP error: {flow.error}")


addons = [SimpleTCPInterceptor()]
