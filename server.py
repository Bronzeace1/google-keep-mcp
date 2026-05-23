"""
Google Keep MCP Server (Python)
Connects Claude to your Google Keep notes via gkeepapi.

Run setup_auth.py once before starting this server.
"""

import asyncio
import keyring
import gkeepapi
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

SERVICE = "google-keep-mcp"

# ---------------------------------------------------------------------------
# Connect to Google Keep using stored token (no password on disk)
# ---------------------------------------------------------------------------
keep = gkeepapi.Keep()

def login():
    email = keyring.get_password(SERVICE, "email")
    token = keyring.get_password(SERVICE, "master_token")

    if not email or not token:
        print(
            "ERROR: No credentials found. Run setup_auth.py first:\n"
            "  py setup_auth.py",
            flush=True,
        )
        return False

    try:
        keep.resume(email, token)
        print(f"Connected to Google Keep as {email}", flush=True)
        return True
    except Exception as e:
        print(f"ERROR: Could not connect to Google Keep: {e}", flush=True)
        print("Try re-running setup_auth.py to refresh your token.", flush=True)
        return False

# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------
app = Server("google-keep-mcp")

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="list_notes",
            description="List notes from Google Keep, with optional search query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Optional search query to filter notes by title or content",
                    }
                },
            },
        ),
        types.Tool(
            name="create_note",
            description="Create a new note in Google Keep",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title of the note"},
                    "content": {"type": "string", "description": "Body text of the note"},
                },
                "required": ["content"],
            },
        ),
        types.Tool(
            name="get_note",
            description="Get the full content of a specific note by its ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "The note ID"},
                },
                "required": ["id"],
            },
        ),
        types.Tool(
            name="delete_note",
            description="Move a Google Keep note to trash",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "The note ID to delete"},
                },
                "required": ["id"],
            },
        ),
        types.Tool(
            name="update_note",
            description="Update the title or content of an existing note",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "The note ID to update"},
                    "title": {"type": "string", "description": "New title (optional)"},
                    "content": {"type": "string", "description": "New content (optional)"},
                },
                "required": ["id"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:

    def note_to_dict(note):
        return {
            "id": note.id,
            "title": note.title or "",
            "content": note.text or "",
            "pinned": note.pinned,
            "archived": note.archived,
            "trashed": note.trashed,
        }

    if name == "list_notes":
        query = arguments.get("query", "").lower()
        keep.sync()
        notes = keep.all()
        results = []
        for note in notes:
            if note.trashed:
                continue
            if query:
                if query not in (note.title or "").lower() and query not in (note.text or "").lower():
                    continue
            results.append(note_to_dict(note))

        if not results:
            return [types.TextContent(type="text", text="No notes found.")]
        return [types.TextContent(type="text", text=str(results))]

    elif name == "create_note":
        title = arguments.get("title", "")
        content = arguments.get("content", "")
        keep.sync()
        note = keep.createNote(title, content)
        keep.sync()
        return [types.TextContent(type="text", text=f"Note created with ID: {note.id}")]

    elif name == "get_note":
        note_id = arguments["id"]
        keep.sync()
        note = keep.get(note_id)
        if note is None:
            return [types.TextContent(type="text", text=f"Note with ID {note_id} not found.")]
        return [types.TextContent(type="text", text=str(note_to_dict(note)))]

    elif name == "delete_note":
        note_id = arguments["id"]
        keep.sync()
        note = keep.get(note_id)
        if note is None:
            return [types.TextContent(type="text", text=f"Note with ID {note_id} not found.")]
        note.trash()
        keep.sync()
        return [types.TextContent(type="text", text=f"Note '{note.title or note_id}' moved to trash.")]

    elif name == "update_note":
        note_id = arguments["id"]
        keep.sync()
        note = keep.get(note_id)
        if note is None:
            return [types.TextContent(type="text", text=f"Note with ID {note_id} not found.")]
        if "title" in arguments:
            note.title = arguments["title"]
        if "content" in arguments:
            note.text = arguments["content"]
        keep.sync()
        return [types.TextContent(type="text", text=f"Note '{note_id}' updated successfully.")]

    else:
        raise ValueError(f"Unknown tool: {name}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
async def main():
    if not login():
        return
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
