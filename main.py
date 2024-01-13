import ssl
import undetected_chromedriver as uc
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ssl._create_default_https_context = ssl._create_unverified_context


def wait_for_element(driver, by, by_value, condition="clickable"):
    wait = WebDriverWait(driver, 30)

    if condition == "clickable":
        return wait.until(EC.element_to_be_clickable((by, by_value)))
    elif condition == "present":
        return wait.until(EC.presence_of_element_located((by, by_value)))


def init_driver():
    options = uc.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    return uc.Chrome(headless=False, use_subprocess=False)


def login_gmail(driver):
    GMAIL_EMAIL = "minfordmeike@gmail.com"
    GMAIL_PASSWORD = "k5GRpMSo"
    GMAIL_RECOVERY_EMAIL = "odunavel@yahoo.com"

    driver.get("https://gmail.com/")

    wait_for_element(driver, by=By.ID, by_value="identifierId", condition="present")
    driver.find_element(By.ID, "identifierId").send_keys(GMAIL_EMAIL)

    wait_for_element(
        driver,
        by=By.XPATH,
        by_value="//*[@id='identifierNext']/div/button",
        condition="clickable",
    )
    driver.find_element(By.XPATH, "//*[@id='identifierNext']/div/button").click()

    wait_for_element(
        driver,
        by=By.XPATH,
        by_value="//*[@id='password']/div[1]/div/div[1]/input",
        condition="clickable",
    )
    driver.find_element(
        By.XPATH, "//*[@id='password']/div[1]/div/div[1]/input"
    ).send_keys(GMAIL_PASSWORD)

    wait_for_element(
        driver,
        by=By.XPATH,
        by_value="//*[@id='passwordNext']/div/button",
        condition="clickable",
    )
    driver.find_element(By.XPATH, "//*[@id='passwordNext']/div/button").click()

    sleep(2)
    driver.get("https://gmail.com/")


def main():
    driver = init_driver()
    login_gmail(driver)
    sleep(20000)


if __name__ == "__main__":
    main()
