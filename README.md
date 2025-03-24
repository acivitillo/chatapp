# Introduction

This is a small implementation of MCP Client in Django. The MCP Server is currently hard coded with the Django client application.

[MCP Documentation](https://modelcontextprotocol.io/)

### How does it work

- The MCP client sends 2 things to OpenAI via API call:
  - The user prompt received from the Django app
  - The list of available MCP Tools
- The OpenAI LLM reads the user prompts and evaluates if any tool from the received list of tools can be utilized
- If the LLM decides to use a tool, it fetches the Python arguments from the user prompt and feeds them to the tool, the tool is then called on the MCP Server side

Note: a tool is a Python function with a `mcp.tool` decorator.

# Screnshots

## Standard ChatGPT response

![standard LLM interaction](docs/images/01.png "standard LLM interaction")

## Using MCP Server Tool for fetching tables

![fetching tables in db](docs/images/02.png "fetching tables in db")

## Using MCP Server Tool for checking sample of data in database table

![fetching sample data](docs/images/03.png "fetching sample data")

## Using MCP Server Tool for creating a bar chart

![bar chart on db data](docs/images/04.png "bar chart on db data")

## Using Explorer Sidebar

![list of MCP servers and tools](docs/images/05.png "list of MCP servers and tools")

# Running the demo

Update the configs:

- `SQLITE_PATH` inside `chatapp/chatapp/mcp/sql.py`
- All other configs in `chatapp/config.py`

Create Environment Variables:

- `OPENAI_KEY` storing the API Key of Open AI

Create a Python virtual environment and install all Python dependencies:

```bash
cd chatapp
uv sync
```

Activate the Python virtual environment:

```bash
.venv\Scripts\activate
```

Run the django server

```bash
python manage.py runserver
```
