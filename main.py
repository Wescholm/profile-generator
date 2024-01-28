from src.infra.selenium.driver import Extension
from src.services.login import Service, Credentials, Gmail, Twitter, Discord
from src.services.profile_manager import ProfileManager, ProfileConfig


def main() -> None:
    profile_config = ProfileConfig(
        name="test3",
        proxy="",
        extensions=[Extension.METAMASK],
        credentials=Credentials(
            gmail=Gmail(email="minfordmeike@gmail.com", password="k5GRpMSo"),
            twitter=Twitter(
                username="LauraSchwa38625",
                token="02aee5020b3daaa1b19477b52e95110b5897bdb4",
            ),
            discord=Discord(
                token="OTI2OTU3NTAwNjU2MzkwMjM2.GV-ZsJ.we9xlVGehMJdom4brEqwPzrHYKUnXFowlKCvXc",
            ),
        ),
    )

    profile_manager = ProfileManager(profile_config)
    profile_manager.login(Service.GMAIL)
    profile_manager.login(Service.TWITTER)
    profile_manager.login(Service.DISCORD)
    profile_manager.exit()
    exit()


if __name__ == "__main__":
    main()
