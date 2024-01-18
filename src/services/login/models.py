from dataclasses import dataclass
from typing import Optional


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
