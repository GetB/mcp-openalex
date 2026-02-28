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

# --- ASGI Middlewares ---

class BearerAuthMiddleware:
    """Validates Authorization: Bearer <MCP_SERVER_TOKEN>.
    If MCP_SERVER_TOKEN is not set, auth is disabled (dev mode).
    """
    def __init__(self, app):
        self.app = app
        self.token = os.environ.get("MCP_SERVER_TOKEN")

    async def __call__(self, scope, receive, send):
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        if not self.token:
            # Dev mode: auth disabled
            await self.app(scope, receive, send)
            return

        headers = dict(scope.get("headers", []))
        auth = headers.get(b"authorization", b"").decode()
        if not auth.startswith("Bearer ") or auth[len("Bearer "):] != self.token:
            await self._reject(send)
            return

        await self.app(scope, receive, send)

    async def _reject(self, send):
        await send({
            "type": "http.response.start",
            "status": 401,
            "headers": [[b"content-type", b"application/json"]],
        })
        await send({
            "type": "http.response.body",
            "body": b'{"error": "Unauthorized"}',
        })


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
_base_app = mcp.http_app(stateless_http=True)
_base_app = ApiKeyMiddleware(_base_app)
app = BearerAuthMiddleware(_base_app)


if __name__ == "__main__":
    import uvicorn

    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("mcp_openalex.main:app", host=host, port=port)
