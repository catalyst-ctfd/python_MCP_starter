# Mango MCP Server

A minimal Model Context Protocol (MCP) server that implements a simple cipher mapping fruit words to numbers.

## Overview

The Mango cipher maps 10 fruit words to digits 0-9:
- mango → 0
- apple → 1  
- banana → 2
- orange → 3
- grape → 4
- peach → 5
- cherry → 6
- lemon → 7
- berry → 8
- melon → 9

## Features

- JSON-RPC 2.0 compliant HTTP server
- Single tool: `decode` - converts fruit words to their corresponding numbers
- Compatible with Claude Code and other MCP clients

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Start the Server

```bash
python mango_mcp_server.py
```

The server runs on `http://localhost:3000` by default.

### Add to Claude Code

```bash
mcp add http://localhost:3000 --name mango-cipher
```

## API

### Methods

- `initialize` - Establish connection and get server capabilities
- `tools/list` - List available tools
- `tools/call` - Execute the decode tool

### Example Request

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "decode",
    "arguments": {
      "word": "apple"
    }
  },
  "id": 1
}
```

### Example Response

```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [{
      "type": "text",
      "text": "1"
    }]
  },
  "id": 1
}
```

## Protocol

- **Protocol Version**: 2024-11-05
- **Transport**: HTTP with JSON-RPC 2.0
- **Default Port**: 3000

## Files

- `mango_mcp_server.py` - Main MCP server implementation
- `requirements.txt` - Python dependencies