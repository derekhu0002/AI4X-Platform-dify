from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_ENV_FILE = Path(__file__).resolve().parents[3] / ".env"


class OpenCTIMCPSettings(BaseSettings):
    """// @ArchitectureID: 1215"""

    opencti_base_url: str = "http://localhost:8080/graphql"
    opencti_api_token: str = ""
    mock_mode: bool = False
    request_timeout_seconds: float = 15.0
    vs1_object_id: str = ""
    vs2_object_id: str = ""
    vs3_object_id: str = ""
    vs4_object_id: str = ""

    model_config = SettingsConfigDict(
        env_prefix="OPENCTI_MCP_",
        env_file=str(ROOT_ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )
