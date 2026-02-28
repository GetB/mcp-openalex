from dotenv import load_dotenv

load_dotenv()

from mcp_openalex import mcp
import mcp_openalex.tools.openalex 

if __name__ == "__main__":
    mcp.run()