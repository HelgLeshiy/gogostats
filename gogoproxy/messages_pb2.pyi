from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GuildHeader(_message.Message):
    __slots__ = ("id", "lvl", "memberCount", "name", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    LVL_FIELD_NUMBER: _ClassVar[int]
    MEMBERCOUNT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: int
    lvl: int
    memberCount: int
    name: str
    description: int
    def __init__(self, id: _Optional[int] = ..., lvl: _Optional[int] = ..., memberCount: _Optional[int] = ..., name: _Optional[str] = ..., description: _Optional[int] = ...) -> None: ...

class GuildPlayerHeader(_message.Message):
    __slots__ = ("name", "id", "lvl", "player_class", "power", "stage", "guildName")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    LVL_FIELD_NUMBER: _ClassVar[int]
    PLAYER_CLASS_FIELD_NUMBER: _ClassVar[int]
    POWER_FIELD_NUMBER: _ClassVar[int]
    STAGE_FIELD_NUMBER: _ClassVar[int]
    GUILDNAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    id: int
    lvl: int
    player_class: int
    power: int
    stage: int
    guildName: str
    def __init__(self, name: _Optional[str] = ..., id: _Optional[int] = ..., lvl: _Optional[int] = ..., player_class: _Optional[int] = ..., power: _Optional[int] = ..., stage: _Optional[int] = ..., guildName: _Optional[str] = ...) -> None: ...

class GuildPlayer(_message.Message):
    __slots__ = ("header", "role", "stage", "power")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    STAGE_FIELD_NUMBER: _ClassVar[int]
    POWER_FIELD_NUMBER: _ClassVar[int]
    header: GuildPlayerHeader
    role: int
    stage: int
    power: int
    def __init__(self, header: _Optional[_Union[GuildPlayerHeader, _Mapping]] = ..., role: _Optional[int] = ..., stage: _Optional[int] = ..., power: _Optional[int] = ...) -> None: ...

class GuildMemberList(_message.Message):
    __slots__ = ("count", "page", "pageSize", "guildPlayers")
    COUNT_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGESIZE_FIELD_NUMBER: _ClassVar[int]
    GUILDPLAYERS_FIELD_NUMBER: _ClassVar[int]
    count: int
    page: int
    pageSize: int
    guildPlayers: _containers.RepeatedCompositeFieldContainer[GuildPlayer]
    def __init__(self, count: _Optional[int] = ..., page: _Optional[int] = ..., pageSize: _Optional[int] = ..., guildPlayers: _Optional[_Iterable[_Union[GuildPlayer, _Mapping]]] = ...) -> None: ...

class GuildInfo(_message.Message):
    __slots__ = ("header", "list")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LIST_FIELD_NUMBER: _ClassVar[int]
    header: GuildHeader
    list: GuildMemberList
    def __init__(self, header: _Optional[_Union[GuildHeader, _Mapping]] = ..., list: _Optional[_Union[GuildMemberList, _Mapping]] = ...) -> None: ...

class GuildHeaderRequest(_message.Message):
    __slots__ = ("token", "playerId", "strangeKey")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    PLAYERID_FIELD_NUMBER: _ClassVar[int]
    STRANGEKEY_FIELD_NUMBER: _ClassVar[int]
    token: str
    playerId: int
    strangeKey: str
    def __init__(self, token: _Optional[str] = ..., playerId: _Optional[int] = ..., strangeKey: _Optional[str] = ...) -> None: ...

class GuildListRequest(_message.Message):
    __slots__ = ("token", "offset", "strangeKey", "playerId", "count")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    STRANGEKEY_FIELD_NUMBER: _ClassVar[int]
    PLAYERID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    token: str
    offset: int
    strangeKey: str
    playerId: int
    count: int
    def __init__(self, token: _Optional[str] = ..., offset: _Optional[int] = ..., strangeKey: _Optional[str] = ..., playerId: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class DragonDmgRequest(_message.Message):
    __slots__ = ("playerId", "userId", "strangeKey", "var_910007", "class_idx", "offset", "count")
    PLAYERID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    STRANGEKEY_FIELD_NUMBER: _ClassVar[int]
    VAR_910007_FIELD_NUMBER: _ClassVar[int]
    CLASS_IDX_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    playerId: int
    userId: str
    strangeKey: str
    var_910007: int
    class_idx: int
    offset: int
    count: int
    def __init__(self, playerId: _Optional[int] = ..., userId: _Optional[str] = ..., strangeKey: _Optional[str] = ..., var_910007: _Optional[int] = ..., class_idx: _Optional[int] = ..., offset: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class DragonPlayer(_message.Message):
    __slots__ = ("header", "damage")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_FIELD_NUMBER: _ClassVar[int]
    header: GuildPlayerHeader
    damage: str
    def __init__(self, header: _Optional[_Union[GuildPlayerHeader, _Mapping]] = ..., damage: _Optional[str] = ...) -> None: ...

class DragonDmgList(_message.Message):
    __slots__ = ("offset", "count", "list")
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    LIST_FIELD_NUMBER: _ClassVar[int]
    offset: int
    count: int
    list: _containers.RepeatedCompositeFieldContainer[DragonPlayer]
    def __init__(self, offset: _Optional[int] = ..., count: _Optional[int] = ..., list: _Optional[_Iterable[_Union[DragonPlayer, _Mapping]]] = ...) -> None: ...
