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
