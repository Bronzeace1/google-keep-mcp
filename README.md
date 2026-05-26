# Google Keep MCP Server

An MCP (Model Context Protocol) server that lets Claude read, create, and manage your Google Keep notes.

## Compatibility

This MCP server works with **Claude Code**, **Claude Cowork**, and **Claude Desktop** only.
It does **not** work with Claude.ai chat — the web chat runs in the cloud and cannot connect to local MCP servers running on your machine.

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