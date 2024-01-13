import ssl
from time import sleep
from selenium.webdriver.common.by import By
from src.infra.selenium import SeleniumDriver

ssl._create_default_https_context = ssl._create_unverified_context


class ProfileGenerator(SeleniumDriver):
    def __init__(self):
        super().__init__()

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
    profile_generator = ProfileGenerator()
    profile_generator.gmail_login()
    sleep(10000)


if __name__ == "__main__":
    main()
