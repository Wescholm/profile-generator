import os
from selenium.webdriver.common.by import By
from src.infra.selenium import SeleniumDriver


class ProfileGenerator(SeleniumDriver):
    PROFILES_MAIN_DIR_PATH = "./profiles"

    def __init__(self, profile_name: str):
        self.profile_name = profile_name
        profile_dir_path = self.init_profile_dir()
        super().__init__(profile_dir_path)

    def init_profile_dir(self):
        os.makedirs(self.PROFILES_MAIN_DIR_PATH, exist_ok=True)
        return os.path.join(self.PROFILES_MAIN_DIR_PATH, self.profile_name)

    def gmail_login(self) -> None:
        GMAIL_EMAIL = "minfordmeike@gmail.com"
        GMAIL_PASSWORD = "k5GRpMSo"

        self.driver.get("https://gmail.com/")
        self.wait_present_element("identifierId", find_by=By.ID).send_keys(GMAIL_EMAIL)
        self.wait_clickable_element("identifierNext", find_by=By.ID).click()
        self.wait_clickable_element(
            "//*[@id='password']/div[1]/div/div[1]/input"
        ).send_keys(GMAIL_PASSWORD)
        self.wait_clickable_element("passwordNext", find_by=By.ID).click()


def main():
    profile_generator = ProfileGenerator(profile_name="test1")
    profile_generator.gmail_login()
    profile_generator.driver.quit()
    exit()


if __name__ == "__main__":
    main()
