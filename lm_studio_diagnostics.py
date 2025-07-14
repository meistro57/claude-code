#!/usr/bin/env python3
"""
LM Studio Diagnostics Script
Comprehensive testing and troubleshooting for LM Studio integration.
"""

import requests
import socket
import subprocess
import time
import json
from typing import List, Tuple, Optional


def test_port_connectivity(host: str = "localhost", ports: List[int] = None) -> List[Tuple[int, bool]]:
    """Test if ports are open."""
    if ports is None:
        ports = [1234, 1235, 8080, 8000, 3000, 5000, 11434]  # Added Ollama port too
    
    results = []
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            sock.close()
            results.append((port, result == 0))
        except Exception:
            results.append((port, False))
    
    return results


def test_lm_studio_api(base_url: str) -> dict:
    """Test LM Studio API endpoints."""
    results = {
        "base_url": base_url,
        "server_running": False,
        "models_endpoint": False,
        "models": [],
        "chat_endpoint": False,
        "error": None
    }
    
    try:
        # Test models endpoint
        response = requests.get(f"{base_url}/v1/models", timeout=5)
        if response.status_code == 200:
            results["server_running"] = True
            results["models_endpoint"] = True
            models_data = response.json()
            results["models"] = models_data.get("data", [])
        else:
            results["error"] = f"Models endpoint returned status {response.status_code}"
            return results
    except requests.exceptions.RequestException as e:
        results["error"] = f"Cannot connect to models endpoint: {e}"
        return results
    
    # Test chat endpoint if we have models
    if results["models"]:
        try:
            model_id = results["models"][0]["id"]
            payload = {
                "model": model_id,
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 5,
                "temperature": 0
            }
            response = requests.post(
                f"{base_url}/v1/chat/completions",
                json=payload,
                timeout=10
            )
            results["chat_endpoint"] = response.status_code == 200
        except Exception as e:
            results["chat_endpoint"] = False
    
    return results


def check_lm_studio_process() -> bool:
    """Check if LM Studio process is running."""
    try:
        # Check for LM Studio process
        result = subprocess.run(
            ["ps", "aux"], 
            capture_output=True, 
            text=True, 
            timeout=5
        )
        
        lm_studio_processes = [
            line for line in result.stdout.lower().split('\n') 
            if 'lmstudio' in line or 'lm-studio' in line
        ]
        
        return len(lm_studio_processes) > 0
    except Exception:
        return False


def get_system_info() -> dict:
    """Get system information for diagnostics."""
    info = {}
    
    try:
        # Get OS info
        with open("/etc/os-release", "r") as f:
            os_info = f.read()
            for line in os_info.split('\n'):
                if line.startswith('PRETTY_NAME='):
                    info["os"] = line.split('=')[1].strip('"')
                    break
    except Exception:
        info["os"] = "Unknown"
    
    try:
        # Get Python version
        import sys
        info["python_version"] = sys.version.split()[0]
    except Exception:
        info["python_version"] = "Unknown"
    
    try:
        # Check if running in WSL
        with open("/proc/version", "r") as f:
            if "microsoft" in f.read().lower():
                info["wsl"] = True
            else:
                info["wsl"] = False
    except Exception:
        info["wsl"] = False
    
    return info


def main():
    print("🔍 LM Studio Diagnostics")
    print("=" * 50)
    
    # System information
    print("\n📊 System Information:")
    sys_info = get_system_info()
    for key, value in sys_info.items():
        print(f"  {key}: {value}")
    
    # Check if LM Studio process is running
    print("\n🔍 Process Check:")
    if check_lm_studio_process():
        print("  ✅ LM Studio process appears to be running")
    else:
        print("  ❌ LM Studio process not found")
    
    # Test port connectivity
    print("\n🌐 Port Connectivity Test:")
    port_results = test_port_connectivity()
    open_ports = []
    
    for port, is_open in port_results:
        if is_open:
            print(f"  ✅ Port {port} is open")
            open_ports.append(port)
        else:
            print(f"  ❌ Port {port} is closed")
    
    # Test LM Studio API on open ports
    if open_ports:
        print("\n🔌 API Testing:")
        for port in open_ports:
            base_url = f"http://localhost:{port}"
            print(f"\nTesting {base_url}:")
            
            api_results = test_lm_studio_api(base_url)
            
            if api_results["server_running"]:
                print(f"  ✅ LM Studio API is running")
                print(f"  ✅ Models endpoint: {len(api_results['models'])} models found")
                
                for model in api_results["models"]:
                    print(f"    - {model.get('id', 'Unknown')}")
                
                if api_results["chat_endpoint"]:
                    print(f"  ✅ Chat endpoint is working")
                else:
                    print(f"  ❌ Chat endpoint failed")
                    
                # Create working configuration
                print(f"\n🎯 Working Configuration Found!")
                print(f"Base URL: {base_url}")
                if api_results["models"]:
                    print(f"Available models: {len(api_results['models'])}")
                    
                return base_url, api_results["models"]
            else:
                print(f"  ❌ Not LM Studio API: {api_results.get('error', 'Unknown error')}")
    else:
        print("\n❌ No open ports found - LM Studio server is not running")
    
    # Troubleshooting guide
    print("\n🛠️  Troubleshooting Guide:")
    print("1. Make sure LM Studio is installed and running")
    print("2. Open LM Studio application")
    print("3. Go to the 'Local Server' tab")
    print("4. Click 'Start Server' button")
    print("5. Make sure you have a model loaded")
    print("6. Check that the server shows as 'Running' with a green indicator")
    print("7. Note the port number shown (usually 1234)")
    
    if sys_info.get("wsl"):
        print("\n⚠️  WSL Detected:")
        print("- Make sure LM Studio is running in Windows, not WSL")
        print("- The server should be accessible from WSL at localhost")
        print("- If issues persist, try running LM Studio with admin privileges")
    
    print("\n📝 Next Steps:")
    print("1. Start LM Studio and the local server")
    print("2. Run this diagnostic script again")
    print("3. Once a working configuration is found, run the integration script")
    
    return None, []


if __name__ == "__main__":
    main()