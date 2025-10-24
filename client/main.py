import json
import socket
import time
from typing import Any
from hexdump import hexdump

import logging

import urllib.request

from google.protobuf.internal.decoder import _DecodeVarint32 # type: ignore
from messages_pb2 import GuildInfo, GuildMemberList, GuildPlayerHeader, GuildHeaderRequest, GuildListRequest, DragonDmgRequest, DragonDmgList

import zlib

import os

logging.basicConfig(level=logging.INFO)

CLASS_MAP = {
    1: "swordbearer",
    2: "wayfarer",
    3: "scholar",
    4: "shadowlash",
    5: "acolyte"
}

def parse_guild_header(message: bytes) -> GuildInfo:
    if message.find(bytes.fromhex("1c02000000")) == -1:
        raise Exception("Cannot parse guild header: command signature not found")
    
    logging.info("GuildInfo message detected!")
    guild_info = GuildInfo()
    payload_start = (
        message.find(bytes.fromhex("1c02000000")) + 13
    )  # Skip the length prefix
    payload = message[payload_start:]
    guild_info.ParseFromString(payload)
    send_payload: dict[str, Any] = {"players": []}
    for member in guild_info.list.guildPlayers:
        send_payload["players"].append(
            {
                "id": member.header.id,
                "nickname": member.header.name,
                "lvl": member.header.lvl,
                "cls": CLASS_MAP[member.header.player_class // 1000],
                "stage": member.stage,
                "power": member.power,
                "guild": guild_info.header.name
            }
        )
        logging.info(
            f"Player Name: {member.header.name}, Level: {member.header.lvl}, Class: {CLASS_MAP[member.header.player_class // 1000]}, Stage: {member.stage}, Power: {member.power}"
        )
    _ = post_json(
        "http://stream1.transcriptic.ru:5997/v1/players/add",
        payload=send_payload,
    )
    return guild_info

def parse_guild_member_list(message: bytes, guild: str) -> GuildMemberList:
    if message.find(bytes.fromhex("1c03000000")) == -1:
        raise Exception("Cannot parse guild member list: command signature not found")
    
    logging.info("GuildMemberList message detected!")
    guild_member_list = GuildMemberList()
    payload_start = (
        message.find(bytes.fromhex("1c03000000")) + 13
    )  # Skip the length prefix
    payload = message[payload_start:]
    guild_member_list.ParseFromString(payload)
    send_payload: dict[str, Any] = {"players": []}
    for member in guild_member_list.guildPlayers:
        send_payload["players"].append(
            {
                "id": member.header.id,
                "nickname": member.header.name,
                "lvl": member.header.lvl,
                "cls": CLASS_MAP[member.header.player_class // 1000],
                "stage": member.stage,
                "power": member.power,
                "guild": guild
            }
        )
        logging.info(
            f"Player Name: {member.header.name}, Level: {member.header.lvl}, Class: {CLASS_MAP[member.header.player_class // 1000]}, Stage: {member.stage}, Power: {member.power}"
        )
    _ = post_json(
        "http://stream1.transcriptic.ru:5997/v1/players/add",
        payload=send_payload,
    )

    return guild_member_list

def parse_dragon_dmg_list(message: bytes) -> DragonDmgList:
    if message.find(bytes.fromhex("10002115")) == -1:
        raise Exception("Cannot parse dragon dmg list: command signature not found")
    
    logging.info("DragonDmgList message detected!")
    dragon_dmg_list = DragonDmgList()
    payload_start = (
        message.find(bytes.fromhex("10002115")) + 12
    )  # Skip the length prefix
    payload = message[payload_start:]
    print(hexdump(payload))
    dragon_dmg_list.ParseFromString(payload)
    send_payload: dict[str, Any] = {"players": []}
    for dragon_player in dragon_dmg_list.list:
        send_payload["players"].append(
            {
                "id": dragon_player.header.id,
                "dmg": dragon_player.damage
            }
        )
        logging.info(
            f"Player id: {dragon_player.header.id}, Damage: {dragon_player.damage}"
        )
    _ = post_json(
        "http://stream1.transcriptic.ru:5997/v1/dragon_damage/add",
        payload=send_payload,
    )

    return dragon_dmg_list

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
    player.ParseFromString(message_data)
    send_payload: dict[str, Any] = {"players": []}
    send_payload["players"].append(
        {
            "id": player.id,
            "nickname": player.name,
            "lvl": player.lvl,
            "cls": CLASS_MAP[player.player_class // 1000],
            "stage": player.stage,
            "power": player.power,
            "guild": "unknown gulid"
        }
    )
    logging.info(
        f"Player Name: {player.name}, Level: {player.lvl}, Class: {CLASS_MAP[player.player_class // 1000]}, Stage: {player.stage}, Power: {player.power}"
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

HOST = "172.65.168.131"  # The server's hostname or IP address

PORT = 9190  # The port used by the server

def send_command(s: socket.socket, character_idx: int, shift: int, command: bytes, payload: bytes):
    checksum = zlib.crc32(payload)
    sequence = bytes.fromhex('00 00 06 00') + (128 + shift + character_idx - 1).to_bytes(1, byteorder='big')
    total = command + bytes.fromhex('000000') + character_idx.to_bytes(1, byteorder='big') + bytes.fromhex('0000') + sequence + checksum.to_bytes(4, byteorder='big') + payload
    size = len(total) + 4
    total = size.to_bytes(4, byteorder='big') + total
    print("Send:")
    print(hexdump(total))
    s.sendall(total)
    data = s.recv(4096)
    print("Receive:")
    print(hexdump(data))
    print()
    return data

def get_guild_header(s: socket.socket, character_idx: int, player_id: int, strange_key: str, token: str):
    guild_header_request = GuildHeaderRequest(token=token, playerId=player_id, strangeKey=strange_key)
    data = guild_header_request.SerializeToString()
    #data = data[4:15] + data[0:4] + data[15:27]
    result = send_command(s, character_idx, 0, bytes.fromhex('17181c02'), data)
    return parse_guild_header(result)


def get_guild_list(s: socket.socket, guild: str, character_idx: int, player_id: int, strange_key: str, token: str, offset: int, count: int):
    guild_list_request = GuildListRequest(token=token, playerId=player_id, strangeKey=strange_key, offset=offset, count=count)
    data = guild_list_request.SerializeToString()
    result = send_command(s, character_idx, 5, bytes.fromhex('17181c03'), data)
    return parse_guild_member_list(result, guild)

def get_dragon_dmg_list(s: socket.socket, character_idx: int, player_id: int, strange_key: str, user_id: str, class_idx: int, offset: int, count: int):
    dragon_dmg_request = DragonDmgRequest(playerId=player_id, userId=user_id, strangeKey=strange_key, var_910007=910007, class_idx=class_idx, offset=offset, count=count)
    data = dragon_dmg_request.SerializeToString()
    result = send_command(s, character_idx, 34, bytes.fromhex('17182115'), data)
    return parse_dragon_dmg_list(result)

CHARACTER_ID = int(os.getenv("CHARACTER_ID", "1270752"))
USER_ID = os.getenv("USER_ID", "342144263")
CHARACTER_IDX = int(os.getenv("CHARACTER_IDX", "5"))
COLLECT_DMG = os.getenv("COLLECT_DMG", "false")

STRANGE_KEY = "vke5LpGnBT"

while(True):
    if COLLECT_DMG == "false":
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            guild_header = get_guild_header(s, CHARACTER_IDX, CHARACTER_ID, STRANGE_KEY, USER_ID)
            total_members = guild_header.list.count
            logging.info(total_members)
            time.sleep(0.5)

            start = 11
            stride = 10

            for offset in range(start, total_members - 1, stride):
                get_guild_list(s, guild_header.header.name, CHARACTER_IDX, CHARACTER_ID, STRANGE_KEY, USER_ID, offset, stride)
                time.sleep(0.5)
    else:
        for class_idx in range(1, 6):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                offset = 1
                stride = 10
                stop = False
                while(not stop):
                    dmg_list = get_dragon_dmg_list(s, CHARACTER_IDX, CHARACTER_ID, STRANGE_KEY, USER_ID, class_idx, offset, stride)
                    if len(dmg_list.list) < 10:
                        stop = True
                    offset += 10
                    time.sleep(0.5)

            time.sleep(10)
        
    time.sleep(30)