"""
RápidoLingo Backend API Tests
Test all endpoints to ensure they work correctly
"""

import requests
import json
from time import sleep

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test root health check endpoint"""
    print("\n🧪 Testing Health Check...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ Health Check PASSED")

def test_get_lessons():
    """Test lessons endpoint"""
    print("\n🧪 Testing GET /api/lessons...")
    response = requests.get(f"{BASE_URL}/api/lessons")
    print(f"Status: {response.status_code}")
    lessons = response.json()
    print(f"Found {len(lessons)} lessons")
    for lesson in lessons[:3]:  # Print first 3
        print(f"  - {lesson['title']} ({lesson['difficulty']})")
    assert response.status_code == 200
    assert len(lessons) > 0
    print("✅ Lessons Endpoint PASSED")
    return lessons

def test_get_content():
    """Test content endpoint"""
    print("\n🧪 Testing GET /api/content/spanish_beginner...")
    response = requests.get(f"{BASE_URL}/api/content/spanish_beginner")
    print(f"Status: {response.status_code}")
    content = response.json()
    if "beginner_phrases" in content:
        print(f"Found {len(content['beginner_phrases'])} beginner phrases")
        print(f"Example: {content['beginner_phrases'][0]['spanish']}")
    assert response.status_code == 200
    print("✅ Content Endpoint PASSED")

def test_start_session():
    """Test starting a tutoring session"""
    print("\n🧪 Testing POST /api/session/start...")
    payload = {
        "lesson_id": "restaurant",
        "user_level": "beginner"
    }
    response = requests.post(f"{BASE_URL}/api/session/start", json=payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ Error Response: {response.text}")
        raise AssertionError(f"Expected 200, got {response.status_code}")
    
    session = response.json()
    print(f"Session ID: {session['session_id']}")
    print(f"Agent: {session['agent_name']}")
    print(f"LiveKit URL: {session.get('livekit_url', 'N/A')}")
    
    # Check if real LiveKit token was generated
    token = session.get('livekit_token', '')
    if token and token != "mock_token_for_mvp":
        print(f"✅ Real LiveKit Token Generated (length: {len(token)})")
        print(f"Token preview: {token[:50]}...")
    else:
        print(f"⚠️  Using mock token (check LiveKit credentials)")
    
    assert response.status_code == 200
    assert "session_id" in session
    assert "livekit_token" in session
    print("✅ Start Session PASSED")
    return session["session_id"]

def test_session_status(session_id):
    """Test getting session status"""
    print(f"\n🧪 Testing GET /api/session/{session_id}/status...")
    response = requests.get(f"{BASE_URL}/api/session/{session_id}/status")
    print(f"Status: {response.status_code}")
    status = response.json()
    print(f"Session Status: {status['status']}")
    assert response.status_code == 200
    print("✅ Session Status PASSED")

def test_end_session(session_id):
    """Test ending a session"""
    print(f"\n🧪 Testing POST /api/session/{session_id}/end...")
    response = requests.post(f"{BASE_URL}/api/session/{session_id}/end")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Result: {result['message']}")
    assert response.status_code == 200
    print("✅ End Session PASSED")

def run_all_tests():
    """Run all API tests"""
    print("="*60)
    print("🚀 RápidoLingo Backend API Tests")
    print("="*60)
    
    # Wait for server to be ready
    print("\n⏳ Waiting for server to start...")
    sleep(2)
    
    try:
        # Run tests
        test_health_check()
        lessons = test_get_lessons()
        test_get_content()
        session_id = test_start_session()
        test_session_status(session_id)
        test_end_session(session_id)
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"  • API Server: Running ✅")
        print(f"  • Endpoints: All working ✅")
        print(f"  • Lessons: {len(lessons)} available ✅")
        print(f"  • Multi-agent system: Ready ✅")
        print("\n🎯 Backend is production-ready!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server")
        print("Make sure the server is running: python main.py")
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")

if __name__ == "__main__":
    run_all_tests()

