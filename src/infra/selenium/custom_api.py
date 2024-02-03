import logging
from enum import IntEnum
from typing import Tuple
from functools import wraps
from dataclasses import dataclass

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.infra.logger import Logger


logger = Logger(name="Selenium API", level=logging.DEBUG).get_logger()


def log_method_call(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        logger.debug(f"Looking for {method.__name__} element with locator {args[0]}")
        return method(*args, **kwargs)

    return wrapper


@dataclass
class ElementCondition:
    PRESENT = "present"
    CLICKABLE = "clickable"

    @classmethod
    def get(cls, condition: str):
        return getattr(cls, condition.upper(), None)


class MatchMode(IntEnum):
    EXACT = 1
    CONTAINS = 2
    STARTS_WITH = 3


class Locator:
    tag: str
    match_mode: MatchMode

    def __init__(self, tag: str, match_mode: MatchMode):
        self.tag = tag
        self.match_mode = match_mode

    def xpath(self, attr: str, value: str) -> Tuple[By, str]:
        path = None
        match self.match_mode:
            case MatchMode.EXACT:
                path = f"//{self.tag}[@{attr}='{value}']"
            case MatchMode.CONTAINS:
                path = f"//{self.tag}[contains(@{attr}, '{value}')]"
            case MatchMode.STARTS_WITH:
                path = f"//{self.tag}[starts-with(@{attr}, '{value}')]"
        return By.XPATH, path

    @staticmethod
    def id(value: str) -> Tuple[By, str]:
        return By.ID, value


class Condition:
    @staticmethod
    @log_method_call
    def clickable(locator):
        return EC.element_to_be_clickable(locator)

    @staticmethod
    @log_method_call
    def present(locator):
        return EC.presence_of_element_located(locator)

    @staticmethod
    @log_method_call
    def all_present(locator):
        return EC.presence_of_all_elements_located(locator)


class SeleniumCustomAPI:
    DEFAULT_TIMEOUT = 30

    def __init__(self, driver):
        self.driver = driver

    class ElementFinder:
        DEFAULT_CONDITION = ElementCondition.PRESENT
        DEFAULT_MATCH_MODE = MatchMode.EXACT
        DEFAULT_FIND_BY = By.XPATH
        DEFAULT_TAG = "*"
        FORBIDDEN_TAGS = ["shape", "__len__"]

        def __init__(self, api, condition_func):
            self.api = api
            self.locator = Locator(self.DEFAULT_TAG, self.DEFAULT_MATCH_MODE)
            self.find_by = self.DEFAULT_FIND_BY
            self.condition_func = condition_func

        def __getattr__(self, attr, *args):
            if hasattr(By, attr.upper()):
                self.find_by = getattr(By, attr.upper())
            elif hasattr(MatchMode, attr.upper()):
                self.locator.match_mode = getattr(MatchMode, attr.upper())
            elif attr not in self.FORBIDDEN_TAGS:
                self.locator.tag = attr
            return self

        def __call__(self, *args):
            locator = self._build_path(*args)
            wait = WebDriverWait(self.api.driver, self.api.DEFAULT_TIMEOUT)
            return wait.until(self.condition_func(locator))

        def _build_path(self, *args) -> Tuple[By, str]:
            match self.find_by:
                case By.XPATH:
                    attr, value = args if len(args) > 1 else ("id", args[0])
                    return self.locator.xpath(attr, value)
                case By.ID:
                    return self.locator.id(args[0])
                case _:
                    raise NotImplementedError(f"Locator {self.find_by} not implemented")

    @property
    def element(self):
        return self.ElementFinder(self, Condition.present)

    @property
    def all_elements(self):
        return self.ElementFinder(self, Condition.all_present)

    @property
    def clickable(self):
        return self.ElementFinder(self, Condition.clickable)

    def wait_for_url_change(self, timeout: int = DEFAULT_TIMEOUT):
        old_url = self.driver.current_url
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.current_url != old_url
        )
