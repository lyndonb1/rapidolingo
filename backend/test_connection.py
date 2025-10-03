"""
Simple test to verify LiveKit credentials and token generation
"""
import os
import sys

# Fix Windows console encoding
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 70)
print("RAPIDOLINGO CONNECTION TEST")
print("=" * 70)

# Step 1: Load config
print("\n[1/5] Loading configuration...")
try:
    import config
    print("[OK] Config loaded")
except Exception as e:
    print(f"[FAIL] Failed to load config: {e}")
    sys.exit(1)

# Step 2: Check environment variables
print("\n[2/5] Checking environment variables...")
url = os.getenv("LIVEKIT_URL")
key = os.getenv("LIVEKIT_API_KEY")
secret = os.getenv("LIVEKIT_API_SECRET")

print(f"  URL:    {url}")
print(f"  Key:    {key}")
print(f"  Secret: {secret[:20]}..." if secret else "  Secret: NOT SET")

if not url or not key or not secret:
    print("[FAIL] Missing credentials!")
    sys.exit(1)
print("[OK] All credentials present")

# Step 3: Test token generation
print("\n[3/5] Testing token generation...")
try:
    from livekit import api
    
    token = api.AccessToken(key, secret)
    token.with_identity("test-student")
    token.with_name("Test Student")
    token.with_grants(api.VideoGrants(
        room_join=True,
        room="test-room",
        can_publish=True,
        can_subscribe=True,
    ))
    
    jwt_token = token.to_jwt()
    print(f"[OK] Token generated: {jwt_token[:60]}...")
    print(f"  Token length: {len(jwt_token)} characters")
    
except Exception as e:
    print(f"[FAIL] Token generation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 4: Decode token to verify contents
print("\n[4/5] Decoding token to verify contents...")
try:
    import jwt
    decoded = jwt.decode(jwt_token, options={"verify_signature": False})
    print(f"  Token issuer (API key): {decoded.get('iss')}")
    print(f"  Identity: {decoded.get('sub')}")
    print(f"  Room: {decoded.get('video', {}).get('room')}")
    
    if decoded.get('iss') == key:
        print("[OK] Token contains correct API key")
    else:
        print(f"[FAIL] Token has wrong API key!")
        print(f"  Expected: {key}")
        print(f"  Got: {decoded.get('iss')}")
        
except Exception as e:
    print(f"[WARN] Could not decode token: {e}")

# Step 5: Test backend API endpoint
print("\n[5/5] Testing backend API session endpoint...")
try:
    import requests
    response = requests.post(
        "http://localhost:8000/api/session/start",
        json={"lesson_id": "restaurant", "user_level": "beginner"},
        timeout=5
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"[OK] Backend API responded successfully")
        print(f"  Session ID: {data.get('session_id')}")
        print(f"  LiveKit URL: {data.get('livekit_url')}")
        print(f"  Token length: {len(data.get('livekit_token', ''))}")
        
        # Decode the returned token
        returned_token = data.get('livekit_token', '')
        if returned_token:
            decoded_return = jwt.decode(returned_token, options={"verify_signature": False})
            print(f"  Returned token API key: {decoded_return.get('iss')}")
            
            if decoded_return.get('iss') == key:
                print("[OK] Backend is using CORRECT credentials")
            else:
                print("[FAIL] Backend is using WRONG credentials!")
                print(f"  Expected: {key}")
                print(f"  Got: {decoded_return.get('iss')}")
    else:
        print(f"[FAIL] Backend returned error {response.status_code}")
        print(f"  Response: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("[FAIL] Cannot connect to backend at http://localhost:8000")
    print("  Make sure backend is running: python main.py")
except Exception as e:
    print(f"[FAIL] Backend test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)

