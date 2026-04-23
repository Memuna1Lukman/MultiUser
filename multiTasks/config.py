from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    hostname : str
    username : str
    password : str
    port: str
    name: str
    secret_key : str
    algorithm: str
    access_token_expire_minutes: int
    model_config = {'env_file': ".env"}


settings = Settings()