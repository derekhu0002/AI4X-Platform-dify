from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_ENV_FILE = Path(__file__).resolve().parents[3] / ".env"


class NotificationMCPSettings(BaseSettings):
    """// @ArchitectureID: 1227"""

    default_formal_recipient: str = "hdhscu@126.com"
    preview_mode: bool = False
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_address: str = ""
    smtp_use_starttls: bool = True

    model_config = SettingsConfigDict(
        env_prefix="NOTIFICATION_MCP_",
        env_file=str(ROOT_ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )
