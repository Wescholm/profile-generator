from abc import ABC, abstractmethod
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from src.infra.selenium.utilities import SeleniumUtilities
from src.infra.logger import Logger
from .models import Credentials


class LoginServiceBase(ABC):
    logger = Logger(__file__).get_logger()

    def __init__(
        self,
        driver: WebDriver,
        credentials: Credentials,
    ):
        self.driver = driver
        self.credentials = credentials

    @abstractmethod
    def is_logged_in(self) -> bool:
        raise NotImplementedError("is_logged_in method not implemented")

    @abstractmethod
    def perform_login(self) -> None:
        raise NotImplementedError("perform_login method not implemented")

    def login(self) -> None:
        service_name = self.__class__.__name__
        self.logger.info(f"Logging into {service_name}...")
        if self.is_logged_in():
            self.logger.info(f"Already logged into {service_name}")
        else:
            self.perform_login()
            if self.is_logged_in():
                self.logger.info(f"Successfully logged into {service_name}")
            else:
                raise Exception(f"Failed to login to {service_name}")


class Gmail(LoginServiceBase, SeleniumUtilities):
    BASE_URL = "https://gmail.com/"

    def __init__(
        self,
        driver: WebDriver,
        credentials: Credentials,
    ):
        super().__init__(driver, credentials)
        SeleniumUtilities.__init__(self, driver)

    def is_logged_in(self) -> bool:
        self.driver.get(self.BASE_URL)
        return "#inbox" in self.driver.current_url

    def perform_login(self) -> None:
        self.wait_present_element("identifierId", find_by=By.ID).send_keys(
            self.credentials.email
        )
        self.wait_clickable_element("identifierNext", find_by=By.ID).click()
        self.wait_clickable_element(
            "//*[@id='password']/div[1]/div/div[1]/input"
        ).send_keys(self.credentials.password)
        self.wait_clickable_element("passwordNext", find_by=By.ID).click()


class Twitter(LoginServiceBase):
    BASE_URL = "https://twitter.com/"

    def is_logged_in(self) -> bool:
        self.driver.get(self.BASE_URL)
        return "/home" in self.driver.current_url

    def perform_login(self) -> None:
        self.driver.add_cookie(
            {
                "name": "auth_token",
                "value": self.credentials.token,
                "domain": ".twitter.com",
            }
        )


class Discord(LoginServiceBase):
    LOGIN_URL = "https://discord.com/login"

    def is_logged_in(self) -> bool:
        self.driver.get(self.LOGIN_URL)
        return "@me" in self.driver.current_url

    def perform_login(self) -> None:
        self.driver.execute_script(
            """
            document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"{}"`
            location.reload();
            """.format(
                self.credentials.token
            )
        )
