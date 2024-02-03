import csv
from typing import Optional
from src.services.login import Service, Credentials, Gmail, Twitter, Discord, Metamask


class CredentialsManager:
    DEFAULT_FILE_PATH = "./credentials.csv"
    HEADERS = ["profile_id", "gmail", "twitter", "discord", "metamask"]

    def __init__(self, file_path: Optional[str] = DEFAULT_FILE_PATH) -> None:
        self.file_path = file_path

    def get_credentials(self, profile_id: str) -> Credentials:
        profile_credentials = self._get_profile_credentials(profile_id)
        return self._parse_profile_credentials(profile_credentials)

    def _get_profile_credentials(self, profile_id: str) -> dict[str, str]:
        credentials = self._read_credentials()
        for credential in credentials:
            if credential["profile_id"] == profile_id:
                return credential
        raise ValueError(f"Profile credentials for id {profile_id} not found")

    def _read_credentials(self) -> list[dict[str, str]]:
        with open(self.file_path, "r") as file:
            reader = csv.DictReader(file, fieldnames=self.HEADERS)
            return list(reader)

    def _parse_profile_credentials(
        self, profile_credentials: dict[str, str]
    ) -> Credentials:
        credentials = Credentials()
        for service_name in Service:
            if service_name.value in profile_credentials:
                credentials[service_name] = self._parse_service_credentials(
                    service_name, profile_credentials[service_name.value]
                )
        return credentials

    def _parse_service_credentials(self, service: Service, credential_str: str):
        match service:
            case Service.GMAIL:
                email, password = credential_str.split(":")
                return Gmail(email, password)
            case Service.TWITTER:
                token, username = credential_str.split(":")
                return Twitter(token, username)
            case Service.DISCORD:
                return Discord(token=credential_str)
            case Service.METAMASK:
                seed, password = credential_str.split(":")
                return Metamask(seed, password)
            case _:
                raise ValueError(f"Invalid service: {service.name}")
