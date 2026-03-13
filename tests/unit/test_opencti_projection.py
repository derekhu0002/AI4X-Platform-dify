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
