import pytest

from mcp import Client

from src.mcp.server import mcp


@pytest.mark.anyio
async def test_mcp_tool_discovery():
    async with Client(mcp) as client:
        result = await client.list_tools()

        names = {
            tool.name
            for tool in result.tools
        }

        assert len(names) == 7

        assert "business_summary" in names
        assert "delivery_summary" in names
        assert "complaint_themes" in names
        assert "delivery_anomalies" in names
        assert "delivery_risk" in names
        assert "forecast_method" in names


@pytest.mark.anyio
async def test_mcp_resource_discovery():
    async with Client(mcp) as client:
        result = await client.list_resources()

        uris = {
            str(resource.uri)
            for resource in result.resources
        }

        assert len(uris) == 3

        assert "retailops://platform" in uris
        assert "retailops://skills" in uris
        assert "retailops://domains" in uris


@pytest.mark.anyio
async def test_mcp_business_summary():
    async with Client(mcp) as client:
        result = await client.call_tool(
            "business_summary",
            {},
        )

        assert result.is_error is False

        text = result.content[0].text

        assert "99092" in text
        assert "13541712.78" in text


@pytest.mark.anyio
async def test_mcp_delivery_summary():
    async with Client(mcp) as client:
        result = await client.call_tool(
            "delivery_summary",
            {},
        )

        assert result.is_error is False

        text = result.content[0].text

        assert "96204" in text
        assert "7823" in text
        assert "8.13" in text


@pytest.mark.anyio
async def test_mcp_platform_resource():
    async with Client(mcp) as client:
        result = await client.read_resource(
            "retailops://platform"
        )

        text = result.contents[0].text

        assert "RetailOps AI" in text
        assert '"skill_count": 19' in text