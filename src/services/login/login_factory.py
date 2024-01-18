from abc import ABC, abstractmethod
from typing import Dict, Type, TypeVar, Generic
from selenium.webdriver.remote.webdriver import WebDriver
from src.models.profile_generator import Credentials
from src.infra import Logger
from service_registry import Service

CredentialType = TypeVar("CredentialType")


class LoginServiceBase(Generic[CredentialType], ABC):
    def __init__(
        self,
        driver: WebDriver,
        logger: Type[Logger.get_logger],
        credentials: CredentialType,
    ):
        self.driver = driver
        self.logger = logger
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
        service: Service, driver: WebDriver, logger: Logger, credentials: CredentialType
    ) -> LoginServiceBase:
        service_cls = LoginServiceFactory.services.get(service)
        if not service_cls:
            raise NotImplementedError(f"Service {service} not supported")
        return service_cls(driver, logger, getattr(credentials, service.value))


class LoginService:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.logger = Logger(__file__).get_logger()

    def login(self, service: Service, credentials: Credentials) -> None:
        login_service = LoginServiceFactory.get_login_service(
            service, self.driver, self.logger, credentials
        )
        login_service.login()
