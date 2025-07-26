# Brazilian Law Research MCP Server

[🇧🇷 Leia em português](README.br.md)

A MCP (Model Context Protocol) server for agent-driven research on Brazilian law using official 
sources.

<a href="https://glama.ai/mcp/servers/@pdmtt/brlaw_mcp_server">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@pdmtt/brlaw_mcp_server/badge" alt="Brazilian Law Research Server MCP server" />
</a>

## Foreword
This server empowers models with scraping capacities, thus making research easier to anyone 
legitimately interested in Brazilian legal matters. 

This facility comes with a price: the risk of overloading the official sources' servers if misused.
Please be sure to keep the load on the sources to a reasonable amount.

## Requirements

- git
- uv (recommended) or Python >= 3.12
- Google Chrome

## How to use

1. Clone the repository:
```bash
git clone https://github.com/pdmtt/brlaw_mcp_server.git
```

2. Install the dependencies
```bash
uv run patchright install
```

3. Setup your MCP client (e.g. Claude Desktop):
```json
{
  "mcpServers": {
    "brlaw_mcp_server": {
      "command": "uv",
      "args": [
        "--directory",
        "/<path>/brlaw_mcp_server",
        "run",
        "serve"
      ]
    }
  }
}
```

### Available Tools

- `StjLegalPrecedentsRequest`: Research legal precedents made by the National High Court of Brazil 
  (STJ) that meet the specified criteria.
- `TstLegalPrecedentsRequest`: Research legal precedents made by the National High Labor Court of 
  Brazil (TST) that meet the specified criteria.
- `StfLegalPrecedentsRequest`: Research legal precedents made by the Supreme Court (STF) that meet 
  the specified criteria.

## Development

### Tooling

The project uses:
- Ruff for linting and formatting.
- BasedPyright for type checking.
- Pytest for testing.

### Language

Resources, tools and prompts related stuff must be written in Portuguese, because this project aims 
to be used by non-dev folks, such as lawyers and law students. 

Technical legal vocabulary is highly dependent on a country's legal tradition and translating it is 
no trivial task.

Development related stuff should stick to English as conventional, such as source code.

## License

This project is licensed under the MIT License - see the LICENSE file for details.