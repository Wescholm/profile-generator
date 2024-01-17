from abc import ABC, abstractmethod
from selenium.webdriver.remote.webdriver import WebDriver
from src.models.profile_generator import Credentials
from src.infra import Logger
from service_registry import Service


class LoginServiceBase(ABC):
    def __init__(
        self,
        driver: WebDriver,
        logger: type(Logger.get_logger),
        credentials: Credentials,
    ):
        self.driver = driver
        self.logger = logger
        self.credentials = credentials

    @abstractmethod
    def is_logged_in(self) -> bool:
        pass

    @abstractmethod
    def login(self) -> None:
        pass


class LoginServiceFactory:
    service_classes = {
        Service.GMAIL: Gmail,
        Service.TWITTER: Twitter,
        Service.DISCORD: Discord,
    }

    @staticmethod
    def get_login_service(
        service: Service, driver: WebDriver, logger: Logger, credentials: Credentials
    ) -> LoginServiceBase:
        service_class = LoginServiceFactory.service_classes.get(service)
        if not service_class:
            raise ValueError(f"Service {service} not supported")
        return service_class(driver, logger, getattr(credentials, service.value))


class LoginService:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.logger = Logger(__file__).get_logger()

    def login(self, service: Service, credentials: Credentials) -> None:
        login_service = LoginServiceFactory.get_login_service(
            service, self.driver, self.logger, credentials
        )
        login_service.login()
