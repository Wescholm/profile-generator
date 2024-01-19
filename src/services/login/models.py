from enum import Enum
from dataclasses import dataclass
from typing import Optional


class Service(Enum):
    GMAIL = "gmail"
    TWITTER = "twitter"
    DISCORD = "discord"


@dataclass
class Gmail:
    email: str
    password: str


@dataclass
class Twitter:
    token: str
    username: Optional[str] = None


@dataclass
class Discord:
    token: str
    username: Optional[str] = None


@dataclass
class Credentials:
    gmail: Gmail
    twitter: Twitter
    discord: Discord
