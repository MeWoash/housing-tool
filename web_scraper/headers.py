from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

def get_random_user_agent() -> str:
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    agent: str = UserAgent(
        software_names=software_names,
        operating_systems=operating_systems,
    ).get_random_user_agent()

    return agent

def get_headers() -> dict[str, str]:
    return {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "pl;q=0.6",
        "priority": "u=0, i",
        "referer": "https://www.google.com/",
        "upgrade-insecure-requests": "1",
        "user-agent": get_random_user_agent(),
    }
