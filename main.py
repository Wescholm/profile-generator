from src.services.login import Service, Credentials, Gmail, Twitter, Discord
from src.services.profile_manager import ProfileManager, ProfileConfig


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
