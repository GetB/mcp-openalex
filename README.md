# OpenAlex MCP Server

Ein Model Context Protocol (MCP) Server, der LLMs den Zugriff auf die OpenAlex API ermöglicht, um wissenschaftliche Literatur zu suchen.

## Voraussetzungen
* Python 3.10+
* Einen kostenlosen OpenAlex API Key (optional, aber stark empfohlen für höhere Limits)

## Installation

1. Installiere die Abhängigkeiten:
   ```bash
   pip install fastmcp httpx python-dotenv pydantic tenacity