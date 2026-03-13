from pydantic_settings import BaseSettings, SettingsConfigDict


class NotificationMCPSettings(BaseSettings):
    """// @ArchitectureID: 1227"""

    default_formal_recipient: str = "hdhscu@126.com"
    preview_mode: bool = True

    model_config = SettingsConfigDict(env_prefix="NOTIFICATION_MCP_", extra="ignore")
