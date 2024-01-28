import os
from typing import Optional
from dataclasses import dataclass
from src.infra import SeleniumDriver, Logger
from src.services.login import LoginService, Credentials


@dataclass
class ProfileConfig:
    name: str
    extensions: Optional[list] = None
    credentials: Optional[Credentials] = None
    proxy: Optional[str] = None


class ProfileManager(SeleniumDriver, LoginService):
    PROFILES_MAIN_DIR_PATH = "./profiles"
    logger = Logger(__file__).get_logger()

    def __init__(self, profile_config: ProfileConfig):
        self.profile_config = profile_config
        super().__init__(
            proxy=profile_config.proxy,
            extensions=profile_config.extensions,
            profile_dir_path=self.profile_dir_path,
        )
        LoginService.__init__(self, self.driver, profile_config.credentials)

    @property
    def profile_dir_path(self) -> str:
        os.makedirs(self.PROFILES_MAIN_DIR_PATH, exist_ok=True)
        return os.path.join(self.PROFILES_MAIN_DIR_PATH, self.profile_config.name)

    def exit(self) -> None:
        self.logger.info("Exiting...")
        self.driver.quit()
