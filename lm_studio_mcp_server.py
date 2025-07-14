#!/usr/bin/env python3
"""
LM Studio MCP Server
Provides MCP tools for interacting with local LM Studio instances.
"""

import json
import os
import sys
from typing import Any, Dict, List
import requests
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)


class LMStudioMCPServer:
    def __init__(self):
        self.base_url = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234")
        self.model_id = os.getenv("LM_STUDIO_MODEL", "")
        self.api_key = "lm-studio"
        
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to LM Studio API."""
        url = f"{self.base_url}/v1/{endpoint}"
        headers = kwargs.get('headers', {})
        headers['Authorization'] = f"Bearer {self.api_key}"
        kwargs['headers'] = headers
        
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    async def health_check(self) -> List[TextContent]:
        """Check if LM Studio server is healthy."""
        try:
            result = self._make_request("GET", "models")
            if "error" in result:
                return [TextContent(
                    type="text",
                    text=f"❌ LM Studio server is not accessible: {result['error']}"
                )]
            
            models = result.get("data", [])
            if not models:
                return [TextContent(
                    type="text",
                    text="⚠️  LM Studio server is running but no models are loaded"
                )]
            
            return [TextContent(
                type="text",
                text=f"✅ LM Studio server is healthy with {len(models)} model(s) loaded"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Error checking server health: {str(e)}"
            )]
    
    async def list_models(self) -> List[TextContent]:
        """List available models."""
        result = self._make_request("GET", "models")
        
        if "error" in result:
            return [TextContent(
                type="text",
                text=f"Error fetching models: {result['error']}"
            )]
        
        models = result.get("data", [])
        if not models:
            return [TextContent(
                type="text",
                text="No models are currently loaded in LM Studio"
            )]
        
        model_list = []
        for model in models:
            model_id = model.get("id", "Unknown")
            model_list.append(f"• {model_id}")
        
        return [TextContent(
            type="text",
            text=f"Available models:\n" + "\n".join(model_list)
        )]
    
    async def get_current_model(self) -> List[TextContent]:
        """Get the currently configured model."""
        if self.model_id:
            return [TextContent(
                type="text",
                text=f"Current model: {self.model_id}"
            )]
        else:
            return [TextContent(
                type="text",
                text="No model is currently configured"
            )]
    
    async def chat_completion(self, message: str, max_tokens: int = 1000, temperature: float = 0.7) -> List[TextContent]:
        """Send a chat completion request to LM Studio."""
        if not self.model_id:
            return [TextContent(
                type="text",
                text="No model is configured. Please set LM_STUDIO_MODEL environment variable."
            )]
        
        payload = {
            "model": self.model_id,
            "messages": [{"role": "user", "content": message}],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        result = self._make_request("POST", "chat/completions", json=payload)
        
        if "error" in result:
            return [TextContent(
                type="text",
                text=f"Error: {result['error']}"
            )]
        
        try:
            content = result["choices"][0]["message"]["content"]
            return [TextContent(
                type="text",
                text=content
            )]
        except (KeyError, IndexError) as e:
            return [TextContent(
                type="text",
                text=f"Error parsing response: {str(e)}"
            )]


async def main():
    server = Server("lmstudio")
    lm_studio = LMStudioMCPServer()
    
    @server.list_tools()
    async def handle_list_tools() -> List[Tool]:
        return [
            Tool(
                name="health_check",
                description="Check if LM Studio server is running and healthy",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            Tool(
                name="list_models",
                description="List all available models in LM Studio",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            Tool(
                name="get_current_model",
                description="Get the currently configured model",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            Tool(
                name="chat_completion",
                description="Send a message to the LM Studio model",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "The message to send to the model"
                        },
                        "max_tokens": {
                            "type": "integer",
                            "description": "Maximum number of tokens to generate",
                            "default": 1000
                        },
                        "temperature": {
                            "type": "number",
                            "description": "Temperature for response generation",
                            "default": 0.7
                        }
                    },
                    "required": ["message"]
                }
            )
        ]
    
    @server.call_tool()
    async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        if name == "health_check":
            return await lm_studio.health_check()
        elif name == "list_models":
            return await lm_studio.list_models()
        elif name == "get_current_model":
            return await lm_studio.get_current_model()
        elif name == "chat_completion":
            message = arguments.get("message", "")
            max_tokens = arguments.get("max_tokens", 1000)
            temperature = arguments.get("temperature", 0.7)
            return await lm_studio.chat_completion(message, max_tokens, temperature)
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="lmstudio",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None
                )
            )
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())