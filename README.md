# Google Keep MCP Server

An MCP (Model Context Protocol) server that lets Claude read, create, and manage your Google Keep notes.

## Tools Available

| Tool | Description |
|------|-------------|
| `list_notes` | List all notes, with optional search query |
| `create_note` | Create a new note with title, content, and labels |
| `get_note` | Fetch a specific note by ID |
| `delete_note` | Move a note to trash |

## Setup

```bash
npm install
node index.js
```

## Status

🚧 Work in progress — tool stubs are in place, Google Keep authentication coming next.
