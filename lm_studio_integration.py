#!/usr/bin/env python3
"""
LM Studio Integration for Claude Code
Provides model discovery and selection for local LM Studio instances.
"""

import json
import requests
import sys
from typing import List, Dict, Optional


class LMStudioClient:
    def __init__(self, base_url: str = "http://localhost:1234"):
        self.base_url = base_url
        self.api_key = "lm-studio"
        
    def is_server_running(self) -> bool:
        """Check if LM Studio server is running."""
        try:
            response = requests.get(f"{self.base_url}/v1/models", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def get_available_models(self) -> List[Dict]:
        """Get list of available models from LM Studio."""
        try:
            response = requests.get(f"{self.base_url}/v1/models", timeout=10)
            if response.status_code == 200:
                return response.json().get("data", [])
            else:
                print(f"Error fetching models: {response.status_code}")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to LM Studio: {e}")
            return []
    
    def select_model(self, models: List[Dict]) -> Optional[str]:
        """Interactive model selection."""
        if not models:
            print("No models available. Please load a model in LM Studio first.")
            return None
        
        print("\nAvailable models:")
        for i, model in enumerate(models, 1):
            model_id = model.get("id", "Unknown")
            print(f"{i}. {model_id}")
        
        while True:
            try:
                choice = input(f"\nSelect model (1-{len(models)}): ").strip()
                if choice.lower() in ['q', 'quit', 'exit']:
                    return None
                
                index = int(choice) - 1
                if 0 <= index < len(models):
                    return models[index]["id"]
                else:
                    print(f"Please enter a number between 1 and {len(models)}")
            except ValueError:
                print("Please enter a valid number or 'q' to quit")
            except KeyboardInterrupt:
                print("\nExiting...")
                return None
    
    def test_model(self, model_id: str) -> bool:
        """Test the selected model with a simple query."""
        try:
            payload = {
                "model": model_id,
                "messages": [{"role": "user", "content": "Hello, respond with just 'OK' if you're working."}],
                "max_tokens": 10,
                "temperature": 0
            }
            
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload,
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                print(f"Model test successful: {content.strip()}")
                return True
            else:
                print(f"Model test failed: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"Error testing model: {e}")
            return False


def create_mcp_config(model_id: str, base_url: str = "http://localhost:1234") -> Dict:
    """Create MCP configuration for LM Studio integration."""
    return {
        "lmstudio": {
            "command": "python3",
            "args": ["/home/mark/claude-code/lm_studio_mcp_server.py"],
            "env": {
                "LM_STUDIO_BASE_URL": base_url,
                "LM_STUDIO_MODEL": model_id
            }
        }
    }


def main():
    print("LM Studio Integration for Claude Code")
    print("====================================")
    
    client = LMStudioClient()
    
    # Check if server is running
    print("Checking LM Studio server...")
    if not client.is_server_running():
        print("❌ LM Studio server is not running or not accessible at http://localhost:1234")
        print("Please:")
        print("1. Start LM Studio")
        print("2. Load a model")
        print("3. Start the local server")
        sys.exit(1)
    
    print("✅ LM Studio server is running")
    
    # Get available models
    print("Fetching available models...")
    models = client.get_available_models()
    
    if not models:
        print("❌ No models found. Please load a model in LM Studio first.")
        sys.exit(1)
    
    # Select model
    selected_model = client.select_model(models)
    if not selected_model:
        print("No model selected. Exiting.")
        sys.exit(1)
    
    print(f"Selected model: {selected_model}")
    
    # Test model
    print("Testing model...")
    if client.test_model(selected_model):
        print("✅ Model is working correctly")
    else:
        print("❌ Model test failed")
        sys.exit(1)
    
    # Create MCP configuration
    print("Creating MCP configuration...")
    mcp_config = create_mcp_config(selected_model)
    
    # Save configuration
    config_path = "/home/mark/.claude/mcp.json"
    try:
        with open(config_path, 'w') as f:
            json.dump(mcp_config, f, indent=2)
        print(f"✅ MCP configuration saved to {config_path}")
    except Exception as e:
        print(f"❌ Error saving configuration: {e}")
        sys.exit(1)
    
    print("\n🎉 LM Studio integration setup complete!")
    print("You can now use Claude Code with your local LM Studio model.")
    print(f"Selected model: {selected_model}")
    print("\nTo use with Claude Code:")
    print("claude --mcp lmstudio 'your prompt here'")


if __name__ == "__main__":
    main()