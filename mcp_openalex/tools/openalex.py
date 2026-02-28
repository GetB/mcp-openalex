import httpx
import os
from datetime import date
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Union
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from fastmcp import Context
from mcp.types import Icon

# Importiere die zentrale MCP-Instanz und den Context aus der eigenen App
from mcp_openalex import mcp
from mcp_openalex.context import openalex_api_key_ctx

BASE_URL = "https://api.openalex.org"

# Globaler HTTP-Client für Connection Pooling
http_client = httpx.AsyncClient(timeout=30.0)

class OpenAlexPublication(BaseModel):
    """Strukturiertes Modell für eine wissenschaftliche Publikation aus OpenAlex."""
    id: str
    title: str
    authors: str
    publication_date: str
    cited_by_count: int
    abstract: str
    doi: Optional[str] = None
    oa_url: Optional[str] = None
    source: Optional[str] = None

# --- HILFSFUNKTIONEN ---

def _get_api_key() -> str | None:
    return openalex_api_key_ctx.get() or os.environ.get("OPENALEX_API_KEY") or None

def _base_params(extra: dict | None = None) -> dict:
    params = {}
    api_key = _get_api_key()
    if api_key:
        params["api_key"] = api_key
    if extra:
        params.update(extra)
    return params

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)),
    reraise=True
)
async def _get(path: str, params: dict, timeout: float = 15.0) -> dict:
    response = await http_client.get(f"{BASE_URL}{path}", params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()

def _decode_abstract(inverted_index: Dict[str, List[int]] | None) -> str:
    if not inverted_index:
        return ""
    max_idx = max((max(indices) for indices in inverted_index.values() if indices), default=-1)
    if max_idx == -1:
        return ""
    words = [""] * (max_idx + 1)
    for word, indices in inverted_index.items():
        for idx in indices:
            words[idx] = word
    return " ".join(words).strip()

def _fmt_authors(authorships: list) -> str:
    names = [a.get("author", {}).get("display_name", "") for a in authorships[:3]]
    result = ", ".join(filter(None, names)) or "n/a"
    if len(authorships) > 3:
        result += " et al."
    return result

def _fmt_error(e: httpx.HTTPStatusError) -> str:
    if e.response.status_code == 429:
        return "Rate limit reached. Add an OPENALEX_API_KEY for higher limits."
    if e.response.status_code in (401, 403):
        return "Authentication error: the provided API key is invalid or expired."
    try:
        detail = e.response.json().get("error", e.response.text[:200])
    except Exception:
        detail = e.response.text[:200]
    return f"OpenAlex API error: HTTP {e.response.status_code} — {detail}"

def _parse_work(item: dict) -> OpenAlexPublication:
    oa_url = None
    if item.get("open_access") and item["open_access"].get("oa_url"):
        oa_url = item["open_access"]["oa_url"]

    source = ((item.get("primary_location") or {}).get("source") or {}).get("display_name")

    return OpenAlexPublication(
        id=item.get("id", "").split("/")[-1],
        title=item.get("display_name") or "Kein Titel verfügbar",
        authors=_fmt_authors(item.get("authorships", [])),
        publication_date=item.get("publication_date", ""),
        cited_by_count=item.get("cited_by_count", 0),
        abstract=_decode_abstract(item.get("abstract_inverted_index")),
        doi=item.get("doi"),
        oa_url=oa_url,
        source=source
    )

# --- MCP TOOLS ---

@mcp.tool(
    name="get_rate_limit",
    description="Check the remaining API budget before making expensive calls.",
    tags=["budget", "rate limit"],
    meta={"version": "1.1.0", "author": "Alex"},
    icons=[Icon(src="https://files.svgcdn.io/streamline/wallet.svg", mimeType="image/svg+xml", sizes=["48x48"])]
)
async def get_rate_limit(ctx: Context) -> str:
    await ctx.debug("Checking OpenAlex rate limit and budget")
    api_key = _get_api_key()

    if not api_key:
        await ctx.info("Running in anonymous mode (no API key)")
        return (
            "No API key configured — running with anonymous rate limits.\n"
            "Anonymous limits: ~100 req/s, no daily budget cap.\n"
            "Configure OPENALEX_API_KEY for budget tracking and higher limits.\n"
        )
    
    try:
        data = await _get("/rate-limit", {"api_key": api_key})
        rl = data.get("rate_limit", {})
        remaining = rl.get("daily_remaining_usd", 0)
        prepaid = rl.get("prepaid_remaining_usd", 0)
        
        budget_ok = (remaining + prepaid) > 0.001
        if budget_ok:
            await ctx.info("Budget OK")
        else:
            await ctx.warning("Budget nearly exhausted")

        return (
            f"Daily budget:    ${rl.get('daily_budget_usd', 0):.2f}\n"
            f"Used today:      ${rl.get('daily_used_usd', 0):.4f}\n"
            f"Remaining:       ${remaining:.4f}\n"
            f"Prepaid balance: ${prepaid:.4f}\n\n"
            f"Status: {'✓ Budget sufficient' if budget_ok else '⚠ Budget nearly exhausted'}"
        )
    except httpx.HTTPStatusError as e:
        await ctx.error(f"Rate limit API error: {e.response.status_code}")
        return _fmt_error(e)
    except Exception as e:
        await ctx.error(f"Network/Retry error: {e}")
        return f"Network or repeated timeout error: {e}"

@mcp.tool(
    name="search_scientific_literature",
    description="Search for academic publications, authors, and institutions.",
    tags=["search", "literature"],
    meta={"version": "1.1.0", "author": "Alex"},
    icons=[Icon(src="https://files.svgcdn.io/streamline/definition-search-book.svg", mimeType="image/svg+xml", sizes=["48x48"])]
)
async def search_scientific_literature(
    ctx: Context,
    search_keywords: List[str] = Field(..., description="Liste englischer wissenschaftlicher Suchbegriffe (z.B. 'meat processing')."),
    start_date: date = Field(..., description="Startdatum zur zeitlichen Eingrenzung (YYYY-MM-DD), z.B. '2024-10-01'."),
    country_codes: Optional[List[str]] = Field(["de", "at", "ch"], description="Zweistellige ISO-Ländercodes. Leer lassen für weltweite Suche."),
    max_results: int = Field(10, description="Maximale Anzahl der Ergebnisse (max 25)."),
    sort: str = Field("cited_by_count:desc", description="Sortierkriterium"),
) -> Union[List[OpenAlexPublication], str]:
    filters = [
        f"from_publication_date:{start_date.isoformat()}",
        "is_oa:true",
        "has_abstract:true"
    ]

    if country_codes:
        countries_str = "|".join(country_codes)
        filters.append(f"authorships.institutions.country_code:{countries_str}")

    search_query = " ".join(search_keywords)
    params = _base_params({
        "filter": ",".join(filters),
        "per_page": min(max_results, 100), 
        "select": "id,display_name,publication_year,publication_date,cited_by_count,authorships,doi,open_access,type,primary_location,abstract_inverted_index",
    })
    
    if search_query:
        params["search"] = search_query
    if sort:
        params["sort"] = sort

    try:
        data = await _get("/works", params=params, timeout=30.0)
        return [_parse_work(item) for item in data.get("results", [])]
    except httpx.HTTPStatusError as e:
        await ctx.error(f"Search API error: {e.response.status_code}")
        return _fmt_error(e)
    except Exception as e:
        await ctx.error(f"Network/Retry error: {e}")
        return f"Network or repeated timeout error: {e}"

@mcp.tool(
    name="semantic_search_literature",
    description="Semantic search for academic publications based on concepts or full text.",
    tags=["semantic search", "literature"],
    meta={"version": "1.1.0", "author": "Alex"},
    icons=[Icon(src="https://files.svgcdn.io/streamline/artificial-intelligence-spark.svg", mimeType="image/svg+xml", sizes=["48x48"])]
)
async def semantic_search_literature(
    ctx: Context,
    query: str = Field(..., description="Vollständiger Text (z.B. Absatz, Forschungsfrage), für den ähnliche Publikationen gesucht werden."),
    max_results: int = Field(5, description="Anzahl der Ergebnisse (max 10, da sehr teuer)."),
) -> Union[List[OpenAlexPublication], str]:
    await ctx.warning(f"Initiating EXPENSIVE semantic search for concept: '{query[:50]}...'")

    params = _base_params({
        "search": query, 
        "per_page": min(max_results, 10), 
        "select": "id,display_name,publication_year,publication_date,cited_by_count,authorships,doi,open_access,type,primary_location,abstract_inverted_index",
    })

    try:
        data = await _get("/find/works", params, timeout=45.0) 
        results = data.get("results", [])
        meta = data.get("meta", {})
        cost = meta.get("cost_usd", 0)
        
        await ctx.info(f"Semantic search completed. Found {len(results)} matches (cost: ${cost:.4f})")
        
        if not results:
            return "No conceptually similar works found for the provided query."
        
        return [_parse_work(item) for item in results]
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            await ctx.error("Semantic search endpoint (/find/works) is unavailable or deprecated.")
            return "Error: Semantic search API unavailable. Fall back to 'search_scientific_literature'."
        return _fmt_error(e)
    except Exception as e:
        await ctx.error(f"Network/Retry error: {e}")
        return f"Network error during semantic search: {e}"