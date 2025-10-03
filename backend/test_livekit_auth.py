"""
Test LiveKit Authentication
"""
import os
import sys

# Import config to set env vars
try:
    import config
    print("[OK] Config loaded")
except ImportError:
    print("[!] Config not found")
    sys.exit(1)

# Check what's in environment
LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")

print("\n" + "="*60)
print("LiveKit Configuration Check")
print("="*60)
print(f"URL:    {LIVEKIT_URL}")
print(f"Key:    {LIVEKIT_API_KEY}")
print(f"Secret: {LIVEKIT_API_SECRET}")
print("="*60)

# Try to create a token to test auth
try:
    from livekit import api
    
    print("\n[Testing] Creating access token...")
    token = api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
    token.with_identity("test-agent")
    token.with_name("Test Agent")
    token.with_grants(api.VideoGrants(
        room_join=True,
        room="test-room"
    ))
    
    jwt_token = token.to_jwt()
    print(f"[OK] Token created successfully!")
    print(f"Token preview: {jwt_token[:50]}...")
    
except Exception as e:
    print(f"[✗] Failed to create token: {e}")
    import traceback
    traceback.print_exc()

