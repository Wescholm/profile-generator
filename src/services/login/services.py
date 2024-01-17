from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from src.models.profile_generator import Credentials
from src.infra.selenium.utilities import SeleniumUtilities
from src.infra import Logger
from login_factory import LoginServiceBase


class Gmail(LoginServiceBase, SeleniumUtilities):
    LOGIN_URL = "https://gmail.com/"

    def __init__(
        self,
        driver: WebDriver,
        logger: type(Logger.get_logger),
        credentials: Credentials.gmail,
    ):
        LoginServiceBase.__init__(self, driver, logger, credentials)
        SeleniumUtilities.__init__(self, driver)

    @property
    def is_logged_in(self) -> bool:
        return "#inbox" in self.driver.current_url

    def login(self) -> None:
        self.logger.info("Logging to google...")
        self.driver.get(self.LOGIN_URL)
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
            self.logger.info("Successfully logged in to Gmail")


class Twitter(LoginServiceBase):
    LOGIN_URL = "https://twitter.com/"

    @property
    def is_logged_in(self) -> bool:
        return True

    def login(self) -> None:
        self.logger.info("Logging to twitter...")
        self.driver.get("https://twitter.com")
        self.driver.add_cookie(
            {
                "name": "auth_token",
                "value": self.credentials.token,
                "domain": ".twitter.com",
            }
        )
        self.driver.get("https://twitter.com/settings/account")
        self.logger.info("Successfully logged in to Twitter")


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
                    self.credentials.discord.token
                )
            )
            if not self.is_logged_in:
                raise Exception("Failed to login to Discord")
