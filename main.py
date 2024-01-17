import os
from selenium.webdriver.common.by import By
from src.infra import SeleniumDriver, Logger
from src.models.profile_generator import (
    ProfileConfig,
    Credentials,
    Gmail,
    Twitter,
    Discord,
)


class ProfileGenerator(SeleniumDriver):
    PROFILES_MAIN_DIR_PATH = "./profiles"
    logger = Logger(__file__).get_logger()

    def __init__(self, profile_config: ProfileConfig):
        self.profile_config = profile_config
        profile_dir_path = self.init_profile_dir()
        super().__init__(profile_dir_path)

    def init_profile_dir(self) -> str:
        os.makedirs(self.PROFILES_MAIN_DIR_PATH, exist_ok=True)
        return os.path.join(self.PROFILES_MAIN_DIR_PATH, self.profile_config.name)

    def gmail_login(self) -> None:
        self.logger.info("Logging to google...")
        gmail_credentials = self.profile_config.credentials.gmail
        email = gmail_credentials.email
        password = gmail_credentials.password

        self.driver.get("https://gmail.com/")

        is_logged_in = "#inbox" in self.driver.current_url
        if is_logged_in:
            self.logger.info("Already logged in to Gmail")
        else:
            self.wait_present_element("identifierId", find_by=By.ID).send_keys(email)
            self.wait_clickable_element("identifierNext", find_by=By.ID).click()
            self.wait_clickable_element(
                "//*[@id='password']/div[1]/div/div[1]/input"
            ).send_keys(password)
            self.wait_clickable_element("passwordNext", find_by=By.ID).click()
            self.logger.info("Successfully logged in to Gmail")

    def twitter_login(self) -> None:
        self.logger.info("Logging to twitter...")
        self.driver.get("https://twitter.com")
        self.driver.add_cookie(
            {
                "name": "auth_token",
                "value": "02aee5020b3daaa1b19477b52e95110b5897bdb4",
                "domain": ".twitter.com",
            }
        )
        self.driver.get("https://twitter.com/settings/account")

    def discord_login(self) -> None:
        self.logger.info("Logging to discord...")
        self.driver.get("https://discord.com/login")
        self.driver.execute_script(
            """
            document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"{}"`
            location.reload();
            """.format(
                self.profile_config.credentials.discord.token
            )
        )


def main() -> None:
    profile_config = ProfileConfig(
        name="test1",
        credentials=Credentials(
            gmail=Gmail(email="minfordmeike@gmail.com", password="k5GRpMSo"),
            twitter=Twitter(username="LauraSchwa38625", token="SpE90vSb4d"),
            discord=Discord(
                token="OTI2OTU3NTAwNjU2MzkwMjM2.GV-ZsJ.we9xlVGehMJdom4brEqwPzrHYKUnXFowlKCvXc",
            ),
        ),
    )

    profile_generator = ProfileGenerator(profile_config)
    profile_generator.twitter_login()
    profile_generator.driver.quit()

    exit()


if __name__ == "__main__":
    main()
