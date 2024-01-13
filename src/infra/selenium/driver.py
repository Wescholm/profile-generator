import ssl
import undetected_chromedriver as uc
from .utilities import SeleniumUtilities

ssl._create_default_https_context = ssl._create_unverified_context


class SeleniumDriver(SeleniumUtilities):
    def __init__(self, profile_dir_path: str):
        options = uc.ChromeOptions()
        options.add_argument(f"--user-data-dir={profile_dir_path}")
        self.driver = uc.Chrome(options=options, headless=False, use_subprocess=False)
        super().__init__(self.driver)
