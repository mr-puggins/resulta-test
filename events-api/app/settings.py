from pydantic import SecretStr
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    third_party_url: str = 'http://localhost:9000'
    scoreboard_endpoint: str = '/scoreboard'
    team_rankings_endpoint: str = '/team-rankings'
    api_key: SecretStr = 'NO_SECRET'


app_settings = AppSettings()
