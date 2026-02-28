from dotenv import load_dotenv

load_dotenv()

from mcp_openalex import mcp
import mcp_openalex.tools.openalex
import mcp_openalex.resources.trades
import mcp_openalex.prompts.handwerk

from fastmcp.server.transforms import PromptsAsTools, ResourcesAsTools

mcp.add_transform(PromptsAsTools(mcp))
mcp.add_transform(ResourcesAsTools(mcp))

if __name__ == "__main__":
    mcp.run()