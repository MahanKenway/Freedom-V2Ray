from enum import Enum


class Protocol(Enum):
    VLESS = "vless"
    VMESS = "vmess"
    TROJAN = "trojan"
    SHADOWSOCKS = "ss"
    MIX = "mix"
