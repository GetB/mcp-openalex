import httpx
import os
from dotenv import load_dotenv
from fastmcp import FastMCP, Context
from context import openalex_api_key_ctx

load_dotenv()
BASE_URL = "https://api.openalex.org"

mcp = FastMCP("OpenAlex MCP Server")

def _get_api_key() -> str | None:
    return openalex_api_key_ctx.get() or os.environ.get("OPENALEX_API_KEY") or None

async def _get(client: httpx.AsyncClient, path: str, params: dict) -> dict:
    response = await client.get(f"{BASE_URL}{path}", params=params, timeout=15.0)
    response.raise_for_status()
    return response.json()

@mcp.tool()
async def get_rate_limit(ctx: Context) -> str:
  """Check the remaining API budget before making expensive calls.

  Call this first when the user's request would trigger multiple search or filter
  operations. Returns remaining USD balance, daily limit, and per-call costs.
  Without an API key, the API still works but budget tracking is unavailable.
  """
  await ctx.debug("Checking OpenAlex rate limit and budget")
  api_key = _get_api_key()

  if not api_key:
    await ctx.info("Running in anonymous mode (no API key)")
    return (
        "No API key configured — running with anonymous rate limits.\n"
        "Anonymous limits: ~100 req/s, no daily budget cap.\n"
        "Configure OPENALEX_API_KEY for budget tracking and higher limits.\n\n"
        "Call costs for reference:\n"
        "  Singleton (get by ID):  free\n"
        "  List / filter:          $0.10 per 1,000 calls\n"
        "  Search (keyword):       $1.00 per 1,000 calls\n"
        "  Semantic search:        $1.00 per 1,000 calls"
    )
  async with httpx.AsyncClient() as client:
    try:
      data = await _get(client, "/rate-limit", {"api_key": api_key})
      rl = data.get("rate_limit", {})
      costs = rl.get("endpoint_costs_usd", {})
      remaining = rl.get("daily_remaining_usd", 0)
      prepaid = rl.get("prepaid_remaining_usd", 0)
      resets_in = rl.get("resets_in_seconds", 0)
      hours, mins = divmod(resets_in // 60, 60)
      
      budget_ok = (remaining + prepaid) > 0.001
      if budget_ok:
        await ctx.info("Budget OK")
      else:
        await ctx.warning("Budget nearly exhausted")

      assessment = "✓ Budget sufficient for queries." if budget_ok else "⚠ Budget nearly exhausted — consider waiting for reset."

      return (
        f"Daily budget:    ${rl.get('daily_budget_usd', 0):.2f}\n"
        f"Used today:      ${rl.get('daily_used_usd', 0):.4f}\n"
        f"Remaining:       ${remaining:.4f}\n"
        f"Prepaid balance: ${prepaid:.4f}\n"
        f"Resets in:       {hours}h {mins}m\n\n"
        f"Per-call costs (USD):\n"
        f"  Singleton:  free\n"
        f"  Filter:     ${costs.get('list', 0.0001):.4f}\n"
        f"  Search:     ${costs.get('search', 0.001):.4f}\n\n"
        f"{assessment}"
      )
    except httpx.HTTPStatusError as e:
      await ctx.error(f"Rate limit API error: {e.response.status_code}")
    except httpx.RequestError as e:
      await ctx.error(f"Network error: {e}")
if __name__ == "__main__":
    mcp.run()