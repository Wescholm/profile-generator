from selenium.webdriver.remote.webdriver import WebDriver
from .models import Service, Credentials
from .services import Metamask, Gmail, Twitter, Discord


class LoginServiceFactory:
    registry = {
        Service.METAMASK: Metamask,
        Service.GMAIL: Gmail,
        Service.TWITTER: Twitter,
        Service.DISCORD: Discord,
    }

    @staticmethod
    def get_login_service(
        service: Service,
        driver: WebDriver,
        credentials: Credentials,
    ):
        service_cls = LoginServiceFactory.registry.get(service)
        if not service_cls:
            raise NotImplementedError(f"Service {service} not supported")
        return service_cls(driver, getattr(credentials, service.value))


class LoginService:
    def __init__(self, driver: WebDriver, credentials: Credentials):
        self.driver = driver
        self.credentials = credentials

    def login(self, service: Service) -> None:
        login_service = LoginServiceFactory.get_login_service(
            service, self.driver, self.credentials
        )
        login_service.login()
