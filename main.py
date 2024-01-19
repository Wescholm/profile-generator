import os
from dataclasses import dataclass
from src.infra import SeleniumDriver, Logger
from src.services.login import LoginService, Service
from src.services.login import Credentials, Gmail, Twitter, Discord


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


def main() -> None:
    profile_config = ProfileConfig(
        name="test1",
        credentials=Credentials(
            gmail=Gmail(email="minfordmeike@gmail.com", password="k5GRpMSo"),
            twitter=Twitter(username="LauraSchwa38625", token="SpE90vSb4d"),
            discord=Discord(
                token="OTI2OTU3NTAwNjU2MzkwMjM2.GV-ZsJ.we9xlVGehMJdom4brEqwPzrHYKUnXFowlKCvXc",
            ),
        ),
    )
    profile_manager = ProfileManager(profile_config)
    profile_manager.login(Service.GMAIL)
    profile_manager.login(Service.TWITTER)
    profile_manager.login(Service.DISCORD)

    exit()


if __name__ == "__main__":
    main()
