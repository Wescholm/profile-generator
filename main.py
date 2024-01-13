import os
from selenium.webdriver.common.by import By
from src.infra.selenium import SeleniumDriver
from src.models.profile_generator import ProfileConfig, Credentials, Gmail


class ProfileGenerator(SeleniumDriver):
    PROFILES_MAIN_DIR_PATH = "./profiles"

    def __init__(self, profile_config: ProfileConfig):
        self.profile_config = profile_config
        profile_dir_path = self.init_profile_dir()
        super().__init__(profile_dir_path)

    def init_profile_dir(self) -> str:
        os.makedirs(self.PROFILES_MAIN_DIR_PATH, exist_ok=True)
        return os.path.join(self.PROFILES_MAIN_DIR_PATH, self.profile_config.name)

    def gmail_login(self) -> None:
        gmail_credentials = self.profile_config.credentials.gmail
        email = gmail_credentials.email
        password = gmail_credentials.password

        self.driver.get("https://gmail.com/")

        is_logged_in = "#inbox" in self.driver.current_url
        if is_logged_in:
            print("Already logged in to Gmail")
        else:
            self.wait_present_element("identifierId", find_by=By.ID).send_keys(email)
            self.wait_clickable_element("identifierNext", find_by=By.ID).click()
            self.wait_clickable_element(
                "//*[@id='password']/div[1]/div/div[1]/input"
            ).send_keys(password)
            self.wait_clickable_element("passwordNext", find_by=By.ID).click()
            print("Successfully logged in to Gmail")


def main() -> None:
    profile_config = ProfileConfig(
        name="test1",
        credentials=Credentials(
            gmail=Gmail(email="minfordmeike@gmail.com", password="k5GRpMSo")
        ),
    )

    profile_generator = ProfileGenerator(profile_config)
    profile_generator.gmail_login()
    profile_generator.driver.quit()

    exit()


if __name__ == "__main__":
    main()
