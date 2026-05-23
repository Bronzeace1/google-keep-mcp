/**
 * Google Keep MCP Server
 * Allows Claude to read, create, and manage Google Keep notes.
 *
 * NOTE: Google Keep does not have an official public API.
 * This server uses the unofficial gkeepapi Python bridge or
 * a placeholder structure ready for your chosen auth method.
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  { name: "google-keep-mcp", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// ---------------------------------------------------------------------------
// Tool definitions
// ---------------------------------------------------------------------------
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "list_notes",
      description: "List all notes from Google Keep",
      inputSchema: {
        type: "object",
        properties: {
          query: {
            type: "string",
            description: "Optional search query to filter notes",
          },
        },
      },
    },
    {
      name: "create_note",
      description: "Create a new note in Google Keep",
      inputSchema: {
        type: "object",
        properties: {
          title: { type: "string", description: "Title of the note" },
          content: { type: "string", description: "Body text of the note" },
          labels: {
            type: "array",
            items: { type: "string" },
            description: "Optional labels/tags for the note",
          },
        },
        required: ["content"],
      },
    },
    {
      name: "get_note",
      description: "Get a specific note by its ID",
      inputSchema: {
        type: "object",
        properties: {
          id: { type: "string", description: "The note ID" },
        },
        required: ["id"],
      },
    },
    {
      name: "delete_note",
      description: "Delete (trash) a note in Google Keep",
      inputSchema: {
        type: "object",
        properties: {
          id: { type: "string", description: "The note ID to delete" },
        },
        required: ["id"],
      },
    },
  ],
}));

// ---------------------------------------------------------------------------
// Tool handlers (stubs — wire up your Keep client here)
// ---------------------------------------------------------------------------
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "list_notes":
      // TODO: call your Google Keep client and return real notes
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(
              [
                {
                  id: "example-id-1",
                  title: "Example Note",
                  content: "This is a placeholder note.",
                  labels: [],
                },
              ],
              null,
              2
            ),
          },
        ],
      };

    case "create_note":
      // TODO: call your Google Keep client to create the note
      return {
        content: [
          {
            type: "text",
            text: `Note created: "${args.title || "(no title)"}" — ${args.content}`,
          },
        ],
      };

    case "get_note":
      // TODO: look up note by args.id
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(
              { id: args.id, title: "Example", content: "Placeholder" },
              null,
              2
            ),
          },
        ],
      };

    case "delete_note":
      // TODO: trash the note by args.id
      return {
        content: [{ type: "text", text: `Note ${args.id} moved to trash.` }],
      };

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

// ---------------------------------------------------------------------------
// Start the server
// ---------------------------------------------------------------------------
const transport = new StdioServerTransport();
await server.connect(transport);
console.error("Google Keep MCP server running on stdio");
