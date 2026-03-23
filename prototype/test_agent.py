"""
Test script to verify ARYA agent setup
Run this before making outbound calls
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

load_dotenv()


def test_environment():
    """Test if environment variables are set."""
    print("\n" + "="*50)
    print("Testing Environment Setup")
    print("="*50)
    
    errors = []
    
    # Check VideoSDK token
    videosdk_token = os.getenv("VIDEOSDK_AUTH_TOKEN")
    if not videosdk_token:
        errors.append("VIDEOSDK_AUTH_TOKEN not set")
    elif videosdk_token == "your_videosdk_auth_token_here":
        errors.append("VIDEOSDK_AUTH_TOKEN is still the placeholder value")
    elif not videosdk_token.startswith("eyJ"):
        errors.append("VIDEOSDK_AUTH_TOKEN doesn't look like a JWT token (should start with 'eyJ')")
    else:
        print("[OK] VIDEOSDK_AUTH_TOKEN is set")
    
    # Check Google API key
    google_key = os.getenv("GOOGLE_API_KEY")
    if not google_key:
        errors.append("GOOGLE_API_KEY not set")
    elif google_key == "your_google_api_key_here":
        errors.append("GOOGLE_API_KEY is still the placeholder value")
    else:
        print("[OK] GOOGLE_API_KEY is set")
    
    return errors


def test_imports():
    """Test if all required packages can be imported."""
    print("\n" + "="*50)
    print("Testing Package Imports")
    print("="*50)
    
    errors = []
    
    try:
        from videosdk.agents import Agent, AgentSession, RealTimePipeline, WorkerJob
        print("[OK] videosdk.agents imported successfully")
    except ImportError as e:
        errors.append(f"Failed to import videosdk.agents: {e}")
    
    try:
        from videosdk.plugins.google import GeminiRealtime, GeminiLiveConfig
        print("[OK] videosdk.plugins.google imported successfully")
    except ImportError as e:
        errors.append(f"Failed to import videosdk.plugins.google: {e}")
    
    try:
        import httpx
        print("[OK] httpx imported successfully")
    except ImportError as e:
        errors.append(f"Failed to import httpx: {e}")
    
    try:
        from agent import ARYAAgent
        print("[OK] ARYAAgent imported successfully")
    except ImportError as e:
        errors.append(f"Failed to import ARYAAgent: {e}")
    
    return errors


def test_file_structure():
    """Test if all required files exist."""
    print("\n" + "="*50)
    print("Testing File Structure")
    print("="*50)
    
    import os
    from pathlib import Path
    
    errors = []
    required_files = [
        "main.py",
        "agent.py",
        "prompts.py",
        "outbound_call.py",
        ".env",
        "requirements.txt",
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"[OK] {file} exists")
        else:
            errors.append(f"{file} not found")
    
    # Check for hold music
    hold_music = Path("audio/hold_music.mp3")
    if hold_music.exists():
        print(f"[OK] Hold music file exists")
    else:
        print(f"[WARN] Hold music file not found (optional - agent will work without it)")
    
    return errors


def test_videosdk_connection():
    """Test VideoSDK API connection."""
    print("\n" + "="*50)
    print("Testing VideoSDK Connection")
    print("="*50)
    
    import httpx
    import os
    
    auth_token = os.getenv("VIDEOSDK_AUTH_TOKEN")
    if not auth_token:
        print("Cannot test connection - VIDEOSDK_AUTH_TOKEN not set")
        return ["VIDEOSDK_AUTH_TOKEN not set"]
    
    async def _test():
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.videosdk.live/v2/sip/gateways",
                    headers={"Authorization": auth_token},
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    gateways = data.get("gateways", [])
                    print(f"[OK] Connected to VideoSDK API")
                    print(f"Found {len(gateways)} gateway(s):")
                    for gw in gateways:
                        print(f"  - {gw.get('gatewayId', 'N/A')}: {gw.get('name', 'N/A')}")
                    return []
                elif response.status_code == 401:
                    print("[FAIL] Authentication failed - token is invalid")
                    return ["VideoSDK token is invalid"]
                else:
                    print(f"[FAIL] API returned status {response.status_code}")
                    return [f"API error: {response.status_code}"]
                    
        except Exception as e:
            print(f"[FAIL] Connection error: {e}")
            return [str(e)]
    
    return asyncio.run(_test())


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("ARYA Agent Setup Test Suite")
    print("="*60)
    
    all_errors = []
    
    all_errors.extend(test_environment())
    all_errors.extend(test_imports())
    all_errors.extend(test_file_structure())
    
    # Only test connection if environment is set up
    if not any("not set" in e or "placeholder" in e for e in all_errors):
        all_errors.extend(test_videosdk_connection())
    else:
        print("\n" + "="*50)
        print("Skipping VideoSDK connection test")
        print("(Fix environment variables first)")
        print("="*50)
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    if not all_errors:
        print("[SUCCESS] All tests passed! ARYA is ready to run.")
        print("\nNext steps:")
        print("1. Start the agent: python main.py")
        print("2. In another terminal, make outbound call:")
        print("   python outbound_call.py +14155551234")
        return 0
    else:
        print(f"[FAIL] Found {len(all_errors)} error(s):")
        for error in all_errors:
            print(f"  - {error}")
        print("\nPlease fix the errors above before running ARYA.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
