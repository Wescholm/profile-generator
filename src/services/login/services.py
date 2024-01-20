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
    def login(self) -> None:
        raise NotImplementedError("login method not implemented")


class Gmail(LoginServiceBase, SeleniumUtilities):
    BASE_URL = "https://gmail.com/"

    def __init__(
        self,
        driver: WebDriver,
        credentials: Credentials,
    ):
        super().__init__(driver, credentials)
        SeleniumUtilities.__init__(self, driver)

    @property
    def is_logged_in(self) -> bool:
        return "#inbox" in self.driver.current_url

    def login(self) -> None:
        self.logger.info("Logging to google...")
        self.driver.get(self.BASE_URL)

        if self.is_logged_in:
            self.logger.info("Already logged in to Gmail")
        else:
            self.wait_present_element("identifierId", find_by=By.ID).send_keys(
                self.credentials.email
            )
            self.wait_clickable_element("identifierNext", find_by=By.ID).click()
            self.wait_clickable_element(
                "//*[@id='password']/div[1]/div/div[1]/input"
            ).send_keys(self.credentials.password)
            self.wait_clickable_element("passwordNext", find_by=By.ID).click()

        if self.is_logged_in:
            self.logger.info("Successfully logged in to Gmail")
        else:
            raise Exception("Failed to login to Gmail")


class Twitter(LoginServiceBase):
    BASE_URL = "https://twitter.com/"

    @property
    def is_logged_in(self) -> bool:
        return "/home" in self.driver.current_url

    def login(self) -> None:
        self.logger.info("Logging to twitter...")
        self.driver.get(self.BASE_URL)

        if self.is_logged_in:
            self.logger.info("Already logged in to Twitter")
        else:
            self.driver.add_cookie(
                {
                    "name": "auth_token",
                    "value": self.credentials.token,
                    "domain": ".twitter.com",
                }
            )
            self.driver.get(self.BASE_URL)

        if self.is_logged_in:
            self.logger.info("Successfully logged in to Twitter")
        else:
            raise Exception("Failed to login to Twitter")



class Discord(LoginServiceBase):
    LOGIN_URL = "https://discord.com/login"

    @property
    def is_logged_in(self) -> bool:
        return "channels/@me" in self.driver.current_url

    def login(self) -> None:
        self.logger.info("Logging to discord...")
        self.driver.get("https://discord.com/login")

        if self.is_logged_in:
            self.logger.info("Already logged in to Discord")
        else:
            self.driver.execute_script(
                """
                document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"{}"`
                location.reload();
                """.format(
                    self.credentials.token
                )
            )

        if self.is_logged_in:
            self.logger.info("Successfully logged in to Discord")
        else:
            raise Exception("Failed to login to Discord")
