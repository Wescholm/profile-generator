from enum import Enum
from dataclasses import dataclass
from typing import Optional, Any


class Service(Enum):
    METAMASK = "metamask"
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
class Metamask:
    seed: str
    password: str


@dataclass
class Credentials:
    gmail: Optional[Gmail] = None
    twitter: Optional[Twitter] = None
    discord: Optional[Discord] = None
    metamask: Optional[Metamask] = None

    def __setitem__(self, key: Service, value: Any) -> None:
        if key == Service.GMAIL:
            self.gmail = value
        elif key == Service.TWITTER:
            self.twitter = value
        elif key == Service.DISCORD:
            self.discord = value
        elif key == Service.METAMASK:
            self.metamask = value
        else:
            raise ValueError(f"Service {key} not supported")
