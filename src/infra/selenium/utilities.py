from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement


class SeleniumUtilities:
    DEFAULT_TIMEOUT = 30
    DEFAULT_FIND_BY = By.XPATH

    def __init__(self, driver):
        self.driver = driver

    def is_element_present(
        self,
        element: str,
        find_by: str = DEFAULT_FIND_BY,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> bool:
        try:
            self.wait_present_element(element, find_by, timeout)
            return True
        except TimeoutException:
            return False

    def wait_clickable_element(
        self,
        element: str,
        find_by: str = DEFAULT_FIND_BY,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> WebElement:
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable((find_by, element)))

    def wait_present_element(
        self,
        element: str,
        find_by: str = DEFAULT_FIND_BY,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> WebElement:
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((find_by, element)))
