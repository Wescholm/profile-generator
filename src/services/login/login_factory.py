from enum import Enum
from abc import ABC, abstractmethod
from typing import Dict, Type, TypeVar, Generic
from selenium.webdriver.remote.webdriver import WebDriver
from src.infra import Logger
from models import Credentials

ServiceCredentials = TypeVar("ServiceCredentials")


class Service(Enum):
    GMAIL = "gmail"
    TWITTER = "twitter"
    DISCORD = "discord"


class LoginServiceBase(Generic[ServiceCredentials], ABC):
    logger = Logger(__file__).get_logger()

    def __init__(
        self,
        driver: WebDriver,
        credentials: ServiceCredentials,
    ):
        self.driver = driver
        self.credentials = credentials

    @abstractmethod
    def is_logged_in(self) -> bool:
        raise NotImplementedError("is_logged_in method not implemented")

    @abstractmethod
    def login(self) -> None:
        raise NotImplementedError("login method not implemented")


class LoginServiceFactory:
    services: Dict[Service, Type[LoginServiceBase]] = {
        service: getattr(Credentials, service.value) for service in Service
    }

    @staticmethod
    def get_login_service(
        service: Service,
        driver: WebDriver,
        credentials: ServiceCredentials,
    ) -> LoginServiceBase:
        service_cls = LoginServiceFactory.services.get(service)
        if not service_cls:
            raise NotImplementedError(f"Service {service} not supported")
        return service_cls(driver, getattr(credentials, service.value))


class LoginService:
    def __init__(self, driver: WebDriver, credentials: ServiceCredentials):
        self.driver = driver
        self.credentials = credentials

    def login(self, service: Service) -> None:
        service_credentials = getattr(self.credentials, service.value)
        login_service = LoginServiceFactory.get_login_service(
            service, self.driver, service_credentials
        )
        login_service.login()
