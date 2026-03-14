from mcp.opencti_mcp.app.models import QueryRequest
from mcp.opencti_mcp.app.service import OpenCTIProjectionService
from mcp.opencti_mcp.app.settings import OpenCTIMCPSettings


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
