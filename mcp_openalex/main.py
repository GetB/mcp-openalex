import os
from dotenv import load_dotenv

load_dotenv()

from mcp_openalex import mcp
import mcp_openalex.tools.openalex
import mcp_openalex.resources.trades
import mcp_openalex.prompts.handwerk

from fastmcp.server.transforms import PromptsAsTools, ResourcesAsTools
from mcp_openalex.context import openalex_api_key_ctx

mcp.add_transform(PromptsAsTools(mcp))
mcp.add_transform(ResourcesAsTools(mcp))

# --- ASGI Middleware ---

class ApiKeyMiddleware:
    """Reads X-OpenAlex-Api-Key header and sets openalex_api_key_ctx.
    Falls back to OPENALEX_API_KEY env var if header is absent.
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] in ("http", "websocket"):
            headers = dict(scope.get("headers", []))
            tenant_key = headers.get(b"x-openalex-api-key", b"").decode() or None
            if tenant_key:
                token = openalex_api_key_ctx.set(tenant_key)
                try:
                    await self.app(scope, receive, send)
                finally:
                    openalex_api_key_ctx.reset(token)
                return

        await self.app(scope, receive, send)


# Build the ASGI app stack (module-level so uvicorn can import it)
_base_app = mcp.http_app(path="/mcp", stateless_http=True)
app = ApiKeyMiddleware(_base_app)


if __name__ == "__main__":
    import uvicorn

    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("mcp_openalex.main:app", host=host, port=port)
