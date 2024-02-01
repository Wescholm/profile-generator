from time import sleep
from abc import ABC, abstractmethod
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from src.infra.selenium.utilities import SeleniumUtilities
from src.infra.logger import Logger
from .models import Credentials


class LoginServiceBase(ABC, SeleniumUtilities):
    LOGIN_URL = None
    logger = Logger(__file__).get_logger()

    def __init__(
        self,
        driver: WebDriver,
        credentials: Credentials,
    ):
        self.driver = driver
        self.credentials = credentials
        SeleniumUtilities.__init__(self, driver)

    @abstractmethod
    def is_logged_in(self) -> bool:
        raise NotImplementedError("is_logged_in method not implemented")

    @abstractmethod
    def perform_login(self) -> None:
        raise NotImplementedError("perform_login method not implemented")

    def login(self) -> None:
        service_name = self.__class__.__name__
        self.driver.get(self.LOGIN_URL)
        self.logger.info(f"Logging into {service_name}...")

        if self.is_logged_in():
            self.logger.info(f"Already logged into {service_name}")
        else:
            self.perform_login()
            if self.is_logged_in():
                self.logger.info(f"Successfully logged into {service_name}")
            else:
                raise Exception(f"Failed to login to {service_name}")


class Gmail(LoginServiceBase):
    LOGIN_URL = "https://gmail.com/"

    def is_logged_in(self) -> bool:
        self.logger.info(self.driver.current_url)
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
        self.wait_for_url_change()


class Twitter(LoginServiceBase):
    LOGIN_URL = "https://twitter.com/"

    def is_logged_in(self) -> bool:
        return "/home" in self.driver.current_url

    def perform_login(self) -> None:
        self.driver.add_cookie(
            {
                "name": "auth_token",
                "value": self.credentials.token,
                "domain": ".twitter.com",
            }
        )
        self.driver.refresh()


class Discord(LoginServiceBase):
    LOGIN_URL = "https://discord.com/channels/@me"

    def is_logged_in(self) -> bool:
        return "channels/@me" in self.driver.current_url

    def perform_login(self) -> None:
        self.driver.execute_script(
            """
            document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"{}"`
            location.reload();
            """.format(
                self.credentials.token
            )
        )
        sleep(3)


class Metamask(LoginServiceBase):
    LOGIN_URL = "chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html"

    def is_logged_in(self) -> bool:
        return self.driver.current_url.endswith("/home.html#")

    def perform_login(self) -> None:
        if self.driver.current_url.endswith("/home.html#unlock"):
            self._unlock_wallet()
        else:
            self._import_wallet()

    def _import_wallet(self) -> None:
        agree_button = self.wait_clickable_element("//input[@type='checkbox']")
        agree_button.click()

        import_wallet_button = self.wait_clickable_element(
            "//button[@data-testid='onboarding-import-wallet']"
        )
        import_wallet_button.click()

        not_allow_metrics_button = self.wait_clickable_element(
            "//button[@data-testid='metametrics-no-thanks']"
        )
        not_allow_metrics_button.click()

        seed_inputs = self.wait_present_elements("//input[@type='password']")
        seeds = self.credentials.seed.split(" ")
        for i in range(12):
            seed_inputs[i].send_keys(seeds[i])

        confirm_button = self.wait_clickable_element(
            "//button[@data-testid='import-srp-confirm']"
        )
        confirm_button.click()

        password_inputs = self.wait_present_elements("//input[@type='password']")
        for password_input in password_inputs:
            password_input.send_keys(self.credentials.password)

        confirm_checkbox = self.wait_clickable_element("//input[@type='checkbox']")
        confirm_checkbox.click()

        import_button = self.wait_clickable_element(
            "//button[starts-with(@data-testid, 'create-password')]"
        )
        import_button.click()

        onboarding_complete_button = self.wait_clickable_element(
            "//button[@data-testid='onboarding-complete-done']"
        )
        onboarding_complete_button.click()

        next_button = self.wait_clickable_element(
            "//button[@data-testid='pin-extension-next']"
        )
        next_button.click()

        done_button = self.wait_clickable_element(
            "//button[@data-testid='pin-extension-done']"
        )
        done_button.click()

    def _unlock_wallet(self) -> None:
        password_input = self.wait_present_element("//input[@type='password']")
        password_input.send_keys(self.credentials.password)

        unlock_button = self.wait_clickable_element(
            "//button[@data-testid='unlock-submit']"
        )
        unlock_button.click()
