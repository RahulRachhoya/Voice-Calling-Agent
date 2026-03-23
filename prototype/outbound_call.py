"""
ARYA Outbound Call Script
Trigger outbound calls via VideoSDK Telephony API
Usage: python outbound_call.py +14155551234
"""

import os
import sys
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()

VIDEOSDK_API_ENDPOINT = "https://api.videosdk.live/v2"


async def make_outbound_call(phone_number: str):
    """Make an outbound call to a phone number."""
    
    auth_token = os.getenv("VIDEOSDK_AUTH_TOKEN")
    if not auth_token:
        print("[ERROR] VIDEOSDK_AUTH_TOKEN not set in .env")
        return False
    
    gateway_id = os.getenv("VIDEOSDK_OUTBOUND_GATEWAY_ID")
    if not gateway_id or gateway_id == "your_outbound_gateway_id_here":
        print("\n[ERROR] VIDEOSDK_OUTBOUND_GATEWAY_ID not configured")
        print("\nTo configure:")
        print("1. Go to VideoSDK Dashboard > Telephony > Outbound Gateways")
        print("2. Copy your Outbound Gateway ID")
        print("3. Add to .env file:")
        print('   VIDEOSDK_OUTBOUND_GATEWAY_ID=gw_xxxxx')
        print("\nNote: Gateway ID starts with 'gw_' (e.g., gw_abc123)")
        return False
    
    # Gateway ID validation - just check if it exists
    if len(gateway_id) < 5:
        print(f"[ERROR] Gateway ID seems too short: {gateway_id}")
        return False
    
    agent_id = os.getenv("AGENT_ID", "ARYA_Careers360")
    
    headers = {
        "Authorization": auth_token,
        "Content-Type": "application/json"
    }
    
    payload = {
        "gatewayId": gateway_id,
        "sipCallTo": phone_number,
        "agentId": agent_id
    }
    
    print(f"\n{'='*60}")
    print(f"Making Outbound Call")
    print(f"{'='*60}")
    print(f"To: {phone_number}")
    print(f"Gateway: {gateway_id}")
    print(f"Agent: {agent_id}")
    print(f"{'='*60}\n")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{VIDEOSDK_API_ENDPOINT}/sip/call",
                headers=headers,
                json=payload,
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                print("[SUCCESS] Call initiated!")
                print(f"  Call ID: {data.get('callId', 'N/A')}")
                print(f"  Status: {data.get('status', 'N/A')}")
                return True
            else:
                print(f"[ERROR] Failed to initiate call")
                print(f"  Status: {response.status_code}")
                print(f"  Response: {response.text}")
                return False
                
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False


def validate_phone_number(phone: str) -> bool:
    """Validate phone number format."""
    if not phone.startswith("+"):
        print("[ERROR] Phone number must start with '+' (E.164 format)")
        print("  Example: +14155551234 (US), +919876543210 (India)")
        return False
    
    digits_only = phone[1:].replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if not digits_only.isdigit():
        print("[ERROR] Phone number must contain only digits (after +)")
        return False
    
    if len(digits_only) < 10:
        print("[ERROR] Phone number too short (minimum 10 digits)")
        return False
    
    return True


def main():
    """Main entry point."""
    print("\n" + "="*60)
    print("ARYA Outbound Calling System")
    print("="*60)
    
    # Check arguments
    if len(sys.argv) < 2:
        print("\n[ERROR] Phone number required")
        print("\nUsage:")
        print("  python outbound_call.py +14155551234")
        print("="*60 + "\n")
        return 1
    
    phone_number = sys.argv[1].strip()
    
    # Validate
    if not validate_phone_number(phone_number):
        return 1
    
    # Make call
    success = asyncio.run(make_outbound_call(phone_number))
    
    print("\n" + "="*60)
    if success:
        print("Call initiated successfully!")
        print("The agent should answer shortly...")
    else:
        print("Failed to initiate call")
        print("\nTroubleshooting:")
        print("  - Ensure agent is running: python main.py")
        print("  - Check VIDEOSDK_AUTH_TOKEN is valid")
        print("  - Configure VIDEOSDK_OUTBOUND_GATEWAY_ID in .env")
    print("="*60 + "\n")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
