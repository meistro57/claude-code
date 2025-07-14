#!/usr/bin/env python3
"""
Simple test script to verify LM Studio integration is working.
"""

import requests
import json

def test_lm_studio():
    base_url = "http://192.168.1.45:1234"
    
    print("🧪 Testing LM Studio Integration")
    print("=" * 40)
    
    # Test 1: Check server is running
    print("1. Testing server connectivity...")
    try:
        response = requests.get(f"{base_url}/v1/models", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
            models = response.json().get("data", [])
            print(f"   Found {len(models)} models")
        else:
            print(f"❌ Server error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False
    
    # Test 2: Test chat with each working model
    print("\n2. Testing chat completions...")
    working_models = []
    
    for model in models:
        model_id = model.get("id", "Unknown")
        if model_id == "text-embedding-nomic-embed-text-v1.5":
            print(f"   Skipping {model_id} (embedding model)")
            continue
            
        print(f"   Testing {model_id}...", end=" ")
        
        try:
            payload = {
                "model": model_id,
                "messages": [{"role": "user", "content": "Say 'WORKING' if you can respond"}],
                "max_tokens": 5,
                "temperature": 0
            }
            
            response = requests.post(
                f"{base_url}/v1/chat/completions",
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                print(f"✅ {content.strip()}")
                working_models.append(model_id)
            else:
                print(f"❌ Error {response.status_code}")
                
        except Exception as e:
            print(f"❌ {str(e)[:50]}...")
    
    # Test 3: Summary
    print(f"\n3. Summary:")
    print(f"   Working models: {len(working_models)}")
    for model in working_models:
        print(f"   - {model}")
    
    if working_models:
        print(f"\n✅ LM Studio integration is working!")
        print(f"   Recommended model: {working_models[0]}")
        print(f"   Base URL: {base_url}")
        return True
    else:
        print(f"\n❌ No working models found")
        return False

if __name__ == "__main__":
    success = test_lm_studio()
    if success:
        print("\n🎉 Integration test passed!")
        print("You can now use Claude Code with your LM Studio models.")
    else:
        print("\n❌ Integration test failed!")
        print("Please check that LM Studio is running and has models loaded.")