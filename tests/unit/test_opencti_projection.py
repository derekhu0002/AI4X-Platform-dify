from mcp.opencti_mcp.app.models import QueryRequest
from mcp.opencti_mcp.app.service import OpenCTIProjectionService
from mcp.opencti_mcp.app.settings import OpenCTIMCPSettings
import httpx
import pytest


async def _query_graph_projection() -> dict[str, object]:
    settings = OpenCTIMCPSettings(mock_mode=True)
    service = OpenCTIProjectionService(settings)
    request = QueryRequest(
        object_id="indicator--vs4",
        projection_profile="graph",
        include_relationships=True,
        relationship_depth=1,
    )
    response = await service.query(request)
    return response.items[0]


def test_graph_projection_contains_relationships() -> None:
    import asyncio

    projected = asyncio.run(_query_graph_projection())
    assert projected["id"] == "indicator--vs4"
    assert projected["relationships"][0]["relationship_type"] == "related-to"


def test_analysis_projection_contains_business_context() -> None:
    import asyncio

    settings = OpenCTIMCPSettings(mock_mode=True)
    service = OpenCTIProjectionService(settings)
    request = QueryRequest(
        object_id="attack-pattern--vs1",
        projection_profile="analysis",
        fields=[
            "primary_asset",
            "deployment_scope",
            "owner_team",
            "business_domain",
            "business_criticality",
            "execution_window",
        ],
        include_relationships=True,
        relationship_depth=1,
    )

    projected = asyncio.run(service.query(request)).items[0]
    assert projected["name"] == "payment-gateway 2.8.0 上线前威胁建模任务"
    assert projected["primary_asset"] == "payment-gateway 2.8.0"
    assert projected["deployment_scope"] == "prod-payment-cluster"
    assert projected["owner_team"] == "payments-team"
    assert projected["business_domain"] == "支付域"
    assert projected["business_criticality"] == "高"
    assert projected["execution_window"] == "上线前"


def test_notification_projection_contains_risk_context_chain() -> None:
    import asyncio

    settings = OpenCTIMCPSettings(mock_mode=True)
    service = OpenCTIProjectionService(settings)
    request = QueryRequest(
        object_id="vulnerability--vs3",
        projection_profile="notification",
        fields=["risk_object", "primary_asset", "deployment_scope", "owner_team"],
        include_relationships=False,
    )

    projected = asyncio.run(service.query(request)).items[0]
    assert projected["risk_object"] == "CVE-2026-XXXX"
    assert projected["primary_asset"] == "api-gateway 4.2.1"
    assert projected["deployment_scope"] == "prod-edge-cluster"
    assert projected["owner_team"] == "finance-bu"


def test_query_maps_opencti_upstream_5xx_to_contract_error() -> None:
    import asyncio

    class DummyAsyncClient:
        def __init__(self, **_: object) -> None:
            pass

        async def __aenter__(self) -> "DummyAsyncClient":
            return self

        async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
            return None

        async def post(self, url: str, json: dict[str, object], headers: dict[str, str]) -> httpx.Response:
            request = httpx.Request("POST", url, json=json, headers=headers)
            return httpx.Response(502, request=request, text="bad gateway")

    settings = OpenCTIMCPSettings(mock_mode=False)
    service = OpenCTIProjectionService(settings)
    request = QueryRequest(object_id="attack-pattern--vs1", projection_profile="summary")

    from mcp.opencti_mcp.app import service as service_module

    original_client = service_module.httpx.AsyncClient
    service_module.httpx.AsyncClient = DummyAsyncClient
    try:
        with pytest.raises(service_module.MCPContractError) as error:
            asyncio.run(service.query(request))
    finally:
        service_module.httpx.AsyncClient = original_client

    assert error.value.code == "CTI-5021"
    assert error.value.status_code == 502
    assert "OpenCTI GraphQL returned 502" in error.value.message


def test_query_maps_opencti_connection_failure_to_contract_error() -> None:
    import asyncio

    class DummyAsyncClient:
        def __init__(self, **_: object) -> None:
            pass

        async def __aenter__(self) -> "DummyAsyncClient":
            return self

        async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
            return None

        async def post(self, url: str, json: dict[str, object], headers: dict[str, str]) -> httpx.Response:
            request = httpx.Request("POST", url, json=json, headers=headers)
            raise httpx.ConnectError("connect failed", request=request)

    settings = OpenCTIMCPSettings(mock_mode=False)
    service = OpenCTIProjectionService(settings)
    request = QueryRequest(object_id="attack-pattern--vs1", projection_profile="summary")

    from mcp.opencti_mcp.app import service as service_module

    original_client = service_module.httpx.AsyncClient
    service_module.httpx.AsyncClient = DummyAsyncClient
    try:
        with pytest.raises(service_module.MCPContractError) as error:
            asyncio.run(service.query(request))
    finally:
        service_module.httpx.AsyncClient = original_client

    assert error.value.code == "CTI-5031"
    assert error.value.status_code == 503
    assert settings.opencti_base_url in error.value.message


def test_query_uses_configured_vs1_object_id_for_live_opencti_lookup() -> None:
    import asyncio

    class DummyAsyncClient:
        captured_payload: dict[str, object] | None = None

        def __init__(self, **_: object) -> None:
            pass

        async def __aenter__(self) -> "DummyAsyncClient":
            return self

        async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
            return None

        async def post(self, url: str, json: dict[str, object], headers: dict[str, str]) -> httpx.Response:
            DummyAsyncClient.captured_payload = json
            request = httpx.Request("POST", url, json=json, headers=headers)
            return httpx.Response(
                200,
                request=request,
                json={
                    "data": {
                        "stixCoreObject": {
                            "id": "internal-opencti-id",
                            "standard_id": "attack-pattern--e99aa92e-f086-55fb-a041-7414e834a383",
                            "entity_type": "Attack-Pattern",
                            "created_at": "2026-03-14T06:51:51.789Z",
                            "updated_at": "2026-03-14T06:51:51.958Z",
                        }
                    }
                },
            )

    settings = OpenCTIMCPSettings(
        mock_mode=False,
        vs1_object_id="attack-pattern--e99aa92e-f086-55fb-a041-7414e834a383",
    )
    service = OpenCTIProjectionService(settings)
    request = QueryRequest(object_id="attack-pattern--vs1", projection_profile="summary")

    from mcp.opencti_mcp.app import service as service_module

    original_client = service_module.httpx.AsyncClient
    service_module.httpx.AsyncClient = DummyAsyncClient
    try:
        response = asyncio.run(service.query(request))
    finally:
        service_module.httpx.AsyncClient = original_client

    assert DummyAsyncClient.captured_payload is not None
    assert DummyAsyncClient.captured_payload["variables"]["id"] == settings.vs1_object_id
    assert response.items[0]["standard_id"] == settings.vs1_object_id
    assert response.items[0]["id"] == "internal-opencti-id"


def test_query_disables_environment_proxy_in_httpx_client() -> None:
    import asyncio

    class DummyAsyncClient:
        captured_init_kwargs: dict[str, object] | None = None

        def __init__(self, **kwargs: object) -> None:
            DummyAsyncClient.captured_init_kwargs = kwargs

        async def __aenter__(self) -> "DummyAsyncClient":
            return self

        async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
            return None

        async def post(self, url: str, json: dict[str, object], headers: dict[str, str]) -> httpx.Response:
            request = httpx.Request("POST", url, json=json, headers=headers)
            return httpx.Response(
                200,
                request=request,
                json={
                    "data": {
                        "stixCoreObject": {
                            "id": "internal-opencti-id",
                            "standard_id": "attack-pattern--e99aa92e-f086-55fb-a041-7414e834a383",
                            "entity_type": "Attack-Pattern",
                            "created_at": "2026-03-14T06:51:51.789Z",
                            "updated_at": "2026-03-14T06:51:51.958Z",
                        }
                    }
                },
            )

    settings = OpenCTIMCPSettings(mock_mode=False)
    service = OpenCTIProjectionService(settings)
    request = QueryRequest(object_id="attack-pattern--vs1", projection_profile="summary")

    from mcp.opencti_mcp.app import service as service_module

    original_client = service_module.httpx.AsyncClient
    service_module.httpx.AsyncClient = DummyAsyncClient
    try:
        asyncio.run(service.query(request))
    finally:
        service_module.httpx.AsyncClient = original_client

    assert DummyAsyncClient.captured_init_kwargs is not None
    assert DummyAsyncClient.captured_init_kwargs["trust_env"] is False


def test_write_bundle_rejects_missing_minimal_fields() -> None:
    import asyncio

    settings = OpenCTIMCPSettings(mock_mode=True)
    service = OpenCTIProjectionService(settings)

    from mcp.opencti_mcp.app import models as model_module
    from mcp.opencti_mcp.app import service as service_module

    request = model_module.BundleWriteRequest(
        bundle={
            "type": "bundle",
            "objects": [
                {
                    "id": "indicator--vs4",
                    "type": "indicator",
                    "pattern_type": "stix",
                    "valid_from": "2026-03-16T00:00:00Z",
                }
            ],
        },
        dry_run=True,
    )

    with pytest.raises(service_module.MCPContractError) as error:
        asyncio.run(service.write_bundle(request))

    assert error.value.code == "MCP-4006"
    assert "pattern" in error.value.message


def test_write_bundle_accepts_minimal_fields_in_dry_run() -> None:
    import asyncio

    settings = OpenCTIMCPSettings(mock_mode=True)
    service = OpenCTIProjectionService(settings)

    from mcp.opencti_mcp.app.models import BundleWriteRequest

    request = BundleWriteRequest(
        bundle={
            "type": "bundle",
            "objects": [
                {
                    "id": "indicator--vs4",
                    "type": "indicator",
                    "pattern": "[ipv4-addr:value = '10.0.0.1']",
                    "pattern_type": "stix",
                    "valid_from": "2026-03-16T00:00:00Z",
                }
            ],
        },
        dry_run=True,
    )

    response = asyncio.run(service.write_bundle(request))
    assert response.accepted is True
    assert response.mode == "dry-run"


def test_query_uses_incident_vs2_alias_for_live_opencti_lookup_and_context() -> None:
    import asyncio

    class DummyAsyncClient:
        captured_payload: dict[str, object] | None = None

        def __init__(self, **_: object) -> None:
            pass

        async def __aenter__(self) -> "DummyAsyncClient":
            return self

        async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
            return None

        async def post(self, url: str, json: dict[str, object], headers: dict[str, str]) -> httpx.Response:
            DummyAsyncClient.captured_payload = json
            request = httpx.Request("POST", url, json=json, headers=headers)
            return httpx.Response(
                200,
                request=request,
                json={
                    "data": {
                        "stixCoreObject": {
                            "id": "internal-grouping-id",
                            "standard_id": "grouping--9c2d35ae-118a-50b0-8a5a-0e0fadc32712",
                            "entity_type": "Grouping",
                            "created_at": "2026-03-14T06:51:51.789Z",
                            "updated_at": "2026-03-14T06:51:51.958Z",
                        }
                    }
                },
            )

    settings = OpenCTIMCPSettings(
        mock_mode=False,
        vs2_object_id="grouping--9c2d35ae-118a-50b0-8a5a-0e0fadc32712",
    )
    service = OpenCTIProjectionService(settings)
    request = QueryRequest(
        object_id="incident--vs2",
        projection_profile="analysis",
        fields=[
            "risk_object",
            "scene_type",
            "severity",
            "priority",
            "task_status",
            "business_impact",
            "target_roles",
            "primary_asset",
            "deployment_scope",
            "owner_team",
            "business_domain",
            "business_criticality",
            "execution_window",
        ],
    )

    from mcp.opencti_mcp.app import service as service_module

    original_client = service_module.httpx.AsyncClient
    service_module.httpx.AsyncClient = DummyAsyncClient
    try:
        response = asyncio.run(service.query(request))
    finally:
        service_module.httpx.AsyncClient = original_client

    assert DummyAsyncClient.captured_payload is not None
    assert DummyAsyncClient.captured_payload["variables"]["id"] == settings.vs2_object_id
    assert response.items[0]["scene_type"] == "运营响应"
    assert response.items[0]["priority"] == "P2"
    assert response.items[0]["owner_team"] == "secops-team"
    assert response.items[0]["standard_id"] == settings.vs2_object_id
