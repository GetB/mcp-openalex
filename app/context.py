from contextvars import ContextVar
from typing import Optional

# Globale Deklaration der ContextVar, strikt isoliert pro asyncio-Task
openalex_api_key_ctx: ContextVar[Optional[str]] = ContextVar("openalex_api_key", default=None)