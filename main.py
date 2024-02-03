from src.infra.selenium.driver import Extension
from src.services.login import Service
from src.services.profile_manager import ProfileManager, ProfileConfig
from src.services.credentials_manager import CredentialsManager


def main() -> None:
    profile_id = "test_profile"
    credentials_manager = CredentialsManager()

    profile_config = ProfileConfig(
        name=profile_id,
        proxy="http://kpcihgqp-rotate:p6rvumutevve@p.webshare.io:80/",
        extensions=[Extension.METAMASK],
        credentials=credentials_manager.get_credentials(profile_id),
    )

    profile_manager = ProfileManager(profile_config)
    profile_manager.login(Service.METAMASK)
    profile_manager.login(Service.GMAIL)
    profile_manager.login(Service.TWITTER)
    profile_manager.login(Service.DISCORD)
    profile_manager.exit()
    exit()


if __name__ == "__main__":
    main()
