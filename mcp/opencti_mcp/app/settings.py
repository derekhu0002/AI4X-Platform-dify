from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenCTIMCPSettings(BaseSettings):
    """// @ArchitectureID: 1215"""

    opencti_base_url: str = "http://localhost:8080/graphql"
    opencti_api_token: str = ""
    mock_mode: bool = True
    request_timeout_seconds: float = 15.0

    model_config = SettingsConfigDict(env_prefix="OPENCTI_MCP_", extra="ignore")
