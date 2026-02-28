from fastmcp import FastMCP

mcp = FastMCP(
  name="OpenAlex MCP Server",
  instructions="""
# OpenAlex MCP Server

Search and retrieve open-access scientific literature via the OpenAlex API,
with a domain model for German trades (Handwerk) built on top.

---

## Authentication

Pass your OpenAlex API key as a request header:
  X-OpenAlex-Api-Key: <your-key>

If omitted the server falls back to the OPENALEX_API_KEY environment variable,
and then to anonymous access (lower rate limits, no budget tracking).

---

## Tools

### get_rate_limit
Check your remaining daily API budget before making expensive calls.

Returns:
- Daily budget (USD)
- Amount used today
- Remaining daily balance
- Prepaid balance

Use this first if you plan to run semantic searches.

---

### search_scientific_literature
Keyword-based search for open-access academic publications via OpenAlex /works.

Parameters:
- search_keywords  (required) List of English scientific search terms,
                   e.g. ["meat processing", "HACCP", "food safety"].
- start_date       (required) Lower publication date bound (YYYY-MM-DD).
- country_codes    (optional) ISO-3166 alpha-2 codes to restrict author
                   affiliations. Default: ["de", "at", "ch"].
                   Pass an empty list for a worldwide search.
- max_results      (optional) Number of results to return (max 25). Default: 10.
- sort             (optional) OpenAlex sort expression.
                   Default: "cited_by_count:desc".

Returns a list of OpenAlexPublication objects with:
  id, title, authors, publication_date, cited_by_count,
  abstract, doi, oa_url (open-access PDF link), source (journal/venue)

Cost: 1 API credit per call (cheap).

---

### semantic_search_literature
Semantic / vector search using OpenAlex /find/works.

Parameters:
- query       (required) A free-text description, research question, or
              full paragraph. The API embeds this text and finds conceptually
              similar works — no need for exact keyword matches.
- max_results (optional) Number of results (max 10). Default: 5.

Returns the same OpenAlexPublication structure as search_scientific_literature.

Cost: ~1 000 API credits per call (very expensive).
      Always call get_rate_limit first and prefer search_scientific_literature.
      Use semantic search only when keyword search yields fewer than 5 relevant
      results or the topic is too broad / ambiguous for keyword matching.

---

## Resources

Resources are also exposed as callable tools via the ResourcesAsTools transform.

### trade://catalog
List all registered German trade profiles grouped by category.

Returns JSON with structure:
{
  "usage": "trade://{slug}",
  "groups": {
    "<category>": [
      { "slug": "<id>", "name": "<display name>", "aliases": [...] }
    ]
  }
}

Categories included:
  Bauhauptgewerbe · Ausbaugewerbe · Handwerk für den gewerblichen Bedarf
  Kraftfahrzeuggewerbe · Gesundheitsgewerbe · Lebensmittelgewerbe
  Handwerke für den privaten Bedarf

Read this resource first to discover the correct slug for a trade before
fetching a full profile.

---

### trade://{slug}
Full profile for a specific German trade.

Replace {slug} with an identifier from trade://catalog (e.g. "fleischer",
"elektrotechniker", "tischler"). Aliases such as "Metzger" or "Elektriker"
are also accepted.

Returns: trade name, description, research topics, and domain-specific
OpenAlex search keywords ready to pass to search_scientific_literature.

---

## Prompts

Prompts are also exposed as callable tools via the PromptsAsTools transform.

### handwerk_recherche(gewerk, thema)
Guided five-step literature research workflow for a German trade topic.

Parameters:
- gewerk  German trade name as spoken by the craftsman
          (e.g. "Fleischer", "Elektriker", "Dachdecker").
- thema   Specific research topic in everyday language
          (e.g. "Räuchern", "Energieeinsparung", "Fachkräftemangel").

The prompt instructs the assistant to:
  1. Look up the correct slug in trade://catalog.
  2. Load domain keywords and topics from trade://{slug}.
  3. Translate the topic into precise English scientific terminology.
  4. Build a Boolean search string and call search_scientific_literature.
  5. Present findings in plain language tailored to the trade context.

---

### semantic_translation_guide()
Reference guide for bridging the gap between craft everyday language and
academic terminology (no parameters required).

Contains a mapping table of common German trade terms and their scientific
equivalents (e.g. "Räuchern" → "PAH reduction · smoke flavoring · curing"),
plus strategy rules for constructing effective OpenAlex queries.

Intended use: call this prompt when search results are poor and you need
help reformulating the query before trying again.

---

## Recommended Workflow

1. Call get_rate_limit  →  verify budget is sufficient.
2. Read trade://catalog  →  identify the correct trade slug.
3. Read trade://{slug}   →  load domain-specific keywords and topics.
4. Call search_scientific_literature with those keywords (cheap).
5. If fewer than 5 relevant results: consult semantic_translation_guide,
   then retry with refined keywords or (as last resort) use
   semantic_search_literature.

For a fully guided experience, invoke the handwerk_recherche prompt directly
and let the assistant execute all steps automatically.
""")

