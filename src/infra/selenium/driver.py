import ssl
import seleniumwire.undetected_chromedriver as uc
from enum import Enum
from typing import List
from .utilities import SeleniumUtilities
from src.utils import unpack_crx

ssl._create_default_https_context = ssl._create_unverified_context


class Extension(Enum):
    METAMASK = "extensions/metamask.crx"


class SeleniumDriver(SeleniumUtilities):
    HOME_URL = "https://nordvpn.com/what-is-my-ip/"

    def __init__(self, **kwargs) -> None:
        options = self._init_chrome_options(**kwargs)
        self.driver = uc.Chrome(headless=False, use_subprocess=False, **options)

        super().__init__(self.driver)
        self.driver.get(self.HOME_URL)

    def _init_chrome_options(
        self, profile_dir_path: str, proxy: str, extensions: List[Extension]
    ):
        proxy_options = None
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")

        if profile_dir_path:
            options.add_argument(f"--user-data-dir={profile_dir_path}")

        for extension in extensions:
            extension_dir = unpack_crx(extension.value)
            options.add_argument(f"--load-extension={extension_dir}")

        if proxy:
            options.add_argument("--ignore-certificate-errors")
            proxy_options = {
                "proxy": {
                    "http": proxy,
                    "https": proxy,
                }
            }

        return {
            "options": options,
            "seleniumwire_options": proxy_options,
        }
