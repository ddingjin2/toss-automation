from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    base_url: str = Field(default="https://www.tossinvest.com", alias="BASE_URL")
    headless: bool = Field(default=True, alias="HEADLESS")
    browser: Literal["chromium", "firefox", "webkit"] = Field(default="chromium", alias="BROWSER")
    viewport_width: int = Field(default=1440, alias="VIEWPORT_WIDTH")
    viewport_height: int = Field(default=900, alias="VIEWPORT_HEIGHT")
    timeout: int = Field(default=10_000, alias="TIMEOUT")

    trace_on_failure: bool = Field(default=True, alias="TRACE_ON_FAILURE")
    video_on_failure: bool = Field(default=True, alias="VIDEO_ON_FAILURE")
    artifact_dir: Path = Field(default=Path("artifacts"), alias="ARTIFACT_DIR")
    default_stock_query: str = Field(default="삼성전자", alias="DEFAULT_STOCK_QUERY")
    mobile_viewport_width: int = Field(default=390, alias="MOBILE_VIEWPORT_WIDTH")
    mobile_viewport_height: int = Field(default=844, alias="MOBILE_VIEWPORT_HEIGHT")

    @field_validator("base_url")
    @classmethod
    def strip_trailing_slash(cls, value: str) -> str:
        return value.rstrip("/")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
