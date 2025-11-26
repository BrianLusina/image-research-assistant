import logging
from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server with a descriptive name
mcp = FastMCP("WikipediaServer")

# Run the MCP server
if __name__ == "__main__":
    logging.getLogger("wikipedia-mcp").setLevel(logging.WARNING)
    mcp.run(transport="stdio")
