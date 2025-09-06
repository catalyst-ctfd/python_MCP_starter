#!/usr/bin/env python3
"""
Minimal MCP Server - Mango Cipher
Decodes fruit words to numbers using JSON-RPC 2.0
"""

import json
from aiohttp import web

class MangoMCPServer:
    def __init__(self, host="0.0.0.0", port=3000):
        self.host = host
        self.port = port
        self.app = web.Application()
        
        # Mango cipher: fruit word to number mapping
        self.mango_cipher = {
            "mango": 0,
            "apple": 1,
            "banana": 2,
            "orange": 3,
            "grape": 4,
            "peach": 5,
            "cherry": 6,
            "lemon": 7,
            "berry": 8,
            "melon": 9
        }
        
        self.setup_routes()
    
    def setup_routes(self):
        # Single JSON-RPC endpoint
        self.app.router.add_post('/', self.handle_jsonrpc)
        self.app.router.add_post('/rpc', self.handle_jsonrpc)
    
    async def handle_jsonrpc(self, request):
        """Handle JSON-RPC 2.0 requests"""
        try:
            data = await request.json()
            
            # Handle batch requests
            if isinstance(data, list):
                results = []
                for req in data:
                    result = await self.process_request(req)
                    if result is not None:
                        results.append(result)
                return web.json_response(results if results else None)
            
            # Handle single request
            result = await self.process_request(data)
            return web.json_response(result) if result else web.Response(status=204)
            
        except json.JSONDecodeError:
            return web.json_response({
                "jsonrpc": "2.0",
                "error": {
                    "code": -32700,
                    "message": "Parse error"
                },
                "id": None
            })
    
    async def process_request(self, req):
        """Process a single JSON-RPC request"""
        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        # Validate JSON-RPC format
        if req.get("jsonrpc") != "2.0":
            return self.error_response(req_id, -32600, "Invalid Request")
        
        # Route methods
        if method == "initialize":
            result = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "mango-cipher",
                    "version": "1.0.0"
                }
            }
            return self.success_response(req_id, result)
        
        elif method == "tools/list":
            result = {
                "tools": [{
                    "name": "decode",
                    "description": "Using the Mango Cipher, convert a fruit word to its number (0-9)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "word": {
                                "type": "string",
                                "description": "Fruit word to decode"
                            }
                        },
                        "required": ["word"]
                    }
                }]
            }
            return self.success_response(req_id, result)
        
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name == "decode":
                word = arguments.get("word", "").lower()
                
                if word not in self.mango_cipher:
                    return self.error_response(req_id, -32602, f"Word '{word}' not in mango cipher")
                
                result = {
                    "content": [{
                        "type": "text",
                        "text": str(self.mango_cipher[word])
                    }]
                }
                return self.success_response(req_id, result)
            else:
                return self.error_response(req_id, -32601, f"Unknown tool: {tool_name}")
        
        else:
            return self.error_response(req_id, -32601, "Method not found")
    
    def success_response(self, req_id, result):
        """Create a JSON-RPC 2.0 success response"""
        if req_id is None:
            return None  # Notification, no response
        return {
            "jsonrpc": "2.0",
            "result": result,
            "id": req_id
        }
    
    def error_response(self, req_id, code, message):
        """Create a JSON-RPC 2.0 error response"""
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": code,
                "message": message
            },
            "id": req_id
        }
    
    def run(self):
        print(f"Mango MCP Server running on {self.host}:{self.port}")
        web.run_app(self.app, host=self.host, port=self.port)

if __name__ == "__main__":
    server = MangoMCPServer()
    server.run()
