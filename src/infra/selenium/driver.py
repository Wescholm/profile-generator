import undetected_chromedriver as uc
from .utilities import SeleniumUtilities


class SeleniumDriver(SeleniumUtilities):
    def __init__(self):
        options = uc.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        self.driver = uc.Chrome(options=options, headless=False, use_subprocess=False)
        super().__init__(self.driver)
