from dataclasses import dataclass


@dataclass
class Gmail:
    email: str
    password: str


@dataclass
class Credentials:
    gmail: Gmail


@dataclass
class ProfileConfig:
    name: str
    credentials: Credentials
