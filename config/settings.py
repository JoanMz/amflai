# config/settings.py
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    serpapi_api_key: str = Field(..., env="SERPAPI_API_KEY")
    excel_file_path: str = Field("data/vivecolombia.xlsx", env="EXCEL_FILE_PATH")
    amadeus_client_id: str = Field(None, env="AMADEUS_CLIENT_ID")
    amadeus_hostname: str = Field(None, env="AMADEUS_HOSTNAME")
    amadeus_client_secret: str = Field(None, env="AMADEUS_CLIENT_SECRET")
    bold_api_key: str = Field(None, env="BOLD_API_KEY")
    acces_key_id: str = Field(None, env="ACCES_KEY_ID")
    acces_key: str = Field(None, env="ACCES_KEY")
    aws_access_key_id: str = Field(None, env="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = Field(None, env="AWS_SECRET_ACCESS_KEY")
    aws_default_region: str = Field(None, env="AWS_DEFAULT_REGION")
    bedrock_model_id: str = Field(None, env="BEDROCK_MODEL_ID")

    class Config:
        env_file = ".env"

settings = Settings()
