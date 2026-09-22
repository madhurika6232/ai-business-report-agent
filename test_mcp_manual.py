import asyncio

from mcp import Client

from src.mcp.server import mcp


async def main():
    """Test RetailOps MCP server through an MCP client."""

    async with Client(mcp) as client:

        # ====================================================
        # DISCOVER TOOLS
        # ====================================================

        tools_result = await client.list_tools()

        tools = tools_result.tools

        print("=== MCP TOOLS ===")

        print(
            "Tool count:",
            len(tools)
        )

        print(
            "Tool names:",
            [
                tool.name
                for tool in tools
            ]
        )


        # ====================================================
        # DISCOVER RESOURCES
        # ====================================================

        resources_result = await client.list_resources()

        resources = resources_result.resources

        print("\n=== MCP RESOURCES ===")

        print(
            "Resource count:",
            len(resources)
        )

        print(
            "Resource URIs:",
            [
                str(resource.uri)
                for resource in resources
            ]
        )


        # ====================================================
        # CALL BUSINESS TOOL
        # ====================================================

        business = await client.call_tool(
            "business_summary",
            {}
        )

        print("\n=== BUSINESS SUMMARY ===")

        print(business)


        # ====================================================
        # CALL DELIVERY TOOL
        # ====================================================

        delivery = await client.call_tool(
            "delivery_summary",
            {}
        )

        print("\n=== DELIVERY SUMMARY ===")

        print(delivery)


        # ====================================================
        # READ PLATFORM RESOURCE
        # ====================================================

        platform = await client.read_resource(
            "retailops://platform"
        )

        print("\n=== PLATFORM RESOURCE ===")

        print(platform)


        # ====================================================
        # VALIDATION
        # ====================================================

        tool_names = {
            tool.name
            for tool in tools
        }

        resource_uris = {
            str(resource.uri)
            for resource in resources
        }


        print("\n=== VALIDATION ===")

        print(
            "Business tool discovered:",
            "business_summary"
            in tool_names
        )

        print(
            "Delivery tool discovered:",
            "delivery_summary"
            in tool_names
        )

        print(
            "Complaint tool discovered:",
            "complaint_themes"
            in tool_names
        )

        print(
            "Anomaly tool discovered:",
            "delivery_anomalies"
            in tool_names
        )

        print(
            "Risk tool discovered:",
            "delivery_risk"
            in tool_names
        )

        print(
            "Forecast tool discovered:",
            "forecast_method"
            in tool_names
        )

        print(
            "Platform resource discovered:",
            "retailops://platform"
            in resource_uris
        )


if __name__ == "__main__":
    asyncio.run(main())