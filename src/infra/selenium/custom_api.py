from enum import IntEnum
from typing import List, Union
from dataclasses import dataclass

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement


@dataclass
class ElementCondition:
    PRESENT = "present"
    CLICKABLE = "clickable"

    @classmethod
    def get(cls, condition: str):
        return getattr(cls, condition.upper(), None)


class ElementMode(IntEnum):
    SINGLE = 1
    MULTIPLE = 2


class MatchMode(IntEnum):
    EXACT = 1
    CONTAINS = 2
    STARTS_WITH = 3


class SeleniumCustomAPI:
    DEFAULT_TIMEOUT = 30
    DEFAULT_FIND_BY = By.XPATH

    def __init__(self, driver):
        self.driver = driver

    class ElementFinder:
        DEFAULT_CONDITION = ElementCondition.PRESENT
        DEFAULT_FIND_BY = By.XPATH
        DEFAULT_MATCH_MODE = MatchMode.EXACT
        DEFAULT_TAG = "*"
        FORBIDDEN_TAGS = ["shape", "__len__"]

        def __init__(self, selenium_utils, element_mode):
            self.selenium_utils = selenium_utils
            self.element_mode = element_mode
            self.match_mode = self.DEFAULT_MATCH_MODE
            self.find_by = self.DEFAULT_FIND_BY
            self.condition = self.DEFAULT_CONDITION
            self.tag = self.DEFAULT_TAG

        def __getattr__(self, attr, *args):
            if ElementCondition.get(attr):
                self.condition = ElementCondition.get(attr)
            elif hasattr(By, attr.upper()):
                self.find_by = getattr(By, attr.upper())
            elif hasattr(MatchMode, attr.upper()):
                self.match_mode = getattr(MatchMode, attr.upper())
            elif attr not in self.FORBIDDEN_TAGS:
                self.tag = attr
            return self

        def __call__(self, *args):
            path = self._build_path(*args)
            match self.element_mode:
                case ElementMode.SINGLE:
                    match self.condition:
                        case ElementCondition.PRESENT:
                            return self.selenium_utils.wait_present_element(
                                path, self.find_by
                            )
                        case ElementCondition.CLICKABLE:
                            return self.selenium_utils.wait_clickable_element(
                                path, self.find_by
                            )
                case ElementMode.MULTIPLE:
                    return self.selenium_utils.wait_present_all_elements(
                        path, find_by=self.find_by
                    )

            raise NotImplementedError(
                f"Condition {self.condition} for find mode {self.element_mode} not implemented"
            )

        def _build_path(self, *args):
            match self.find_by:
                case By.XPATH:
                    attr, value = args if len(args) > 1 else ("id", args[0])
                    return self._build_xpath(attr, value)
                case By.ID:
                    return args[0]

        def _build_xpath(self, attr: str, value: str) -> str:
            match self.match_mode:
                case MatchMode.EXACT:
                    return f"//{self.tag}[@{attr}='{value}']"
                case MatchMode.CONTAINS:
                    return f"//{self.tag}[contains(@{attr}, '{value}')]"
                case MatchMode.STARTS_WITH:
                    return f"//{self.tag}[starts-with(@{attr}, '{value}')]"

    @property
    def element(self):
        return self.ElementFinder(self, ElementMode.SINGLE)

    @property
    def elements(self):
        return self.ElementFinder(self, ElementMode.MULTIPLE)

    def wait_for_url_change(self, timeout: int = DEFAULT_TIMEOUT):
        old_url = self.driver.current_url
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.current_url != old_url
        )

    def wait_clickable_element(
        self,
        path: str,
        find_by: str = DEFAULT_FIND_BY,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> WebElement:
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable((find_by, path)))

    def wait_present_element(
        self,
        path: str,
        find_by: str = DEFAULT_FIND_BY,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> Union[WebElement, List[WebElement]]:
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((find_by, path)))

    def wait_present_all_elements(
        self,
        path: str,
        find_by: str = DEFAULT_FIND_BY,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> List[WebElement]:
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_all_elements_located((find_by, path)))
