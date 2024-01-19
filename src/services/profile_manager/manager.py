import os
from dataclasses import dataclass
from src.infra import SeleniumDriver, Logger
from src.services.login import LoginService, Credentials


@dataclass
class ProfileConfig:
    name: str
    credentials: Credentials


class ProfileManager(SeleniumDriver, LoginService):
    PROFILES_MAIN_DIR_PATH = "./profiles"
    logger = Logger(__file__).get_logger()

    def __init__(self, profile_config: ProfileConfig):
        self.profile_config = profile_config
        super().__init__(self.profile_dir_path)
        LoginService.__init__(self, self.driver)

    @property
    def profile_dir_path(self) -> str:
        os.makedirs(self.PROFILES_MAIN_DIR_PATH, exist_ok=True)
        return os.path.join(self.PROFILES_MAIN_DIR_PATH, self.profile_config.name)
