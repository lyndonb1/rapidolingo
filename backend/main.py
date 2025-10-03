"""
RápidoLingo Backend - FastAPI Server
Spanish learning at human speed with multi-agent voice tutoring
"""

import os
import json
import uuid
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from livekit import api

# Load environment variables
load_dotenv()

# Import configuration (sets environment variables)
try:
    import config
    print("[✓] Config loaded successfully")
    print(f"[✓] LIVEKIT_URL: {os.getenv('LIVEKIT_URL')}")
    print(f"[✓] LIVEKIT_API_KEY: {os.getenv('LIVEKIT_API_KEY')}")
except ImportError as e:
    print(f"[!] Config not found: {e}")
    print("[!] Will use environment variables")

app = FastAPI(
    title="RápidoLingo API",
    description="Spanish learning at human speed",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        os.getenv("FRONTEND_URL", "http://localhost:3000"),
        "https://*.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class Lesson(BaseModel):
    id: str
    title: str
    description: str
    difficulty: str
    agent_type: str
    category: str

class SessionRequest(BaseModel):
    lesson_id: str
    user_level: str = "beginner"

class SessionResponse(BaseModel):
    session_id: str
    livekit_token: str
    livekit_url: str
    agent_name: str

# Load Spanish content
def load_spanish_content():
    """Load all Spanish learning content from JSON files"""
    context_dir = Path("../context")
    content = {}
    
    for json_file in context_dir.glob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            content[json_file.stem] = json.load(f)
    
    return content

spanish_content = load_spanish_content()

# Helper Functions
def generate_livekit_token(room_name: str, participant_identity: str) -> Optional[str]:
    """Generate LiveKit access token for a participant"""
    api_key = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")
    
    print(f"[DEBUG] Generating token with key: {api_key}")
    print(f"[DEBUG] Room: {room_name}, Participant: {participant_identity}")
    
    # For MVP without LiveKit credentials, return mock token
    if not api_key or not api_secret:
        print("[WARNING] Missing LiveKit credentials - returning mock token")
        return "mock_token_for_mvp"
    
    try:
        token = api.AccessToken(api_key, api_secret) \
            .with_identity(participant_identity) \
            .with_name(f"Student {participant_identity[:8]}") \
            .with_grants(api.VideoGrants(
                room_join=True,
                room=room_name,
                can_publish=True,
                can_subscribe=True,
            ))
        jwt_token = token.to_jwt()
        print(f"[✓] Token generated successfully: {jwt_token[:50]}...")
        return jwt_token
    except Exception as e:
        print(f"[ERROR] Failed to generate LiveKit token: {e}")
        import traceback
        traceback.print_exc()
        return None

# Routes
@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "healthy",
        "app": "RápidoLingo API",
        "version": "1.0.0",
        "message": "Spanish learning at human speed ⚡"
    }

@app.get("/api/lessons", response_model=List[Lesson])
async def get_lessons():
    """Get all available lesson scenarios"""
    lessons = [
        {
            "id": "restaurant",
            "title": "Restaurant Conversation",
            "description": "Order food, ask for recommendations, request the check",
            "difficulty": "beginner",
            "agent_type": "restaurant",
            "category": "travel"
        },
        {
            "id": "airport",
            "title": "Airport Check-in",
            "description": "Check luggage, get boarding pass, find your gate",
            "difficulty": "beginner",
            "agent_type": "airport",
            "category": "travel"
        },
        {
            "id": "hotel",
            "title": "Hotel Booking",
            "description": "Check in, ask about amenities, request services",
            "difficulty": "beginner",
            "agent_type": "hotel",
            "category": "travel"
        },
        {
            "id": "directions",
            "title": "Asking for Directions",
            "description": "Find places, understand directions, navigate the city",
            "difficulty": "beginner",
            "agent_type": "directions",
            "category": "travel"
        },
        {
            "id": "shopping",
            "title": "Shopping",
            "description": "Ask for sizes, colors, prices, and make purchases",
            "difficulty": "intermediate",
            "agent_type": "social",
            "category": "daily_life"
        },
        {
            "id": "social_meetup",
            "title": "Meeting New People",
            "description": "Introductions, small talk, making plans",
            "difficulty": "beginner",
            "agent_type": "social",
            "category": "social"
        },
        {
            "id": "social_party",
            "title": "At a Party",
            "description": "Casual conversations, mingling, expressing opinions",
            "difficulty": "intermediate",
            "agent_type": "social",
            "category": "social"
        },
        {
            "id": "exam_prep",
            "title": "Oral Exam Practice",
            "description": "Common exam questions, strategies, pronunciation tips",
            "difficulty": "intermediate",
            "agent_type": "teacher",
            "category": "academic"
        }
    ]
    return lessons

@app.get("/api/content/{content_type}")
async def get_content(content_type: str):
    """Get specific Spanish content by type"""
    if content_type not in spanish_content:
        raise HTTPException(status_code=404, detail=f"Content type '{content_type}' not found")
    
    return spanish_content[content_type]

@app.post("/api/session/start", response_model=SessionResponse)
async def start_session(request: SessionRequest):
    """
    Start a new tutoring session with LiveKit room creation
    Creates a unique room and returns access token for frontend
    """
    # Generate unique identifiers
    session_id = f"session_{uuid.uuid4().hex[:12]}"
    room_name = f"rapidolingo_{request.lesson_id}_{session_id}"
    participant_id = f"student_{uuid.uuid4().hex[:8]}"
    
    # Agent mapping
    agent_names = {
        "restaurant": "Restaurant Agent (María)",
        "airport": "Airport Agent (Carlos)",
        "hotel": "Hotel Agent (Sofia)",
        "directions": "Directions Agent (Miguel)",
        "social": "Social Agent (Ana)",
        "teacher": "Teacher Agent (Profesora López)"
    }
    
    # Get lesson details
    lessons_response = await get_lessons()
    lesson = next((l for l in lessons_response if l["id"] == request.lesson_id), None)
    
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    agent_name = agent_names.get(lesson["agent_type"], "Teacher Agent")
    
    # Generate LiveKit access token
    token = generate_livekit_token(room_name, participant_id)
    if not token:
        raise HTTPException(status_code=500, detail="Failed to generate session token")
    
    livekit_url = os.getenv("LIVEKIT_URL", "ws://localhost:7880")
    
    print(f"[✓] Session created:")
    print(f"    - Session ID: {session_id}")
    print(f"    - Room: {room_name}")
    print(f"    - LiveKit URL: {livekit_url}")
    print(f"    - Agent: {agent_name}")
    
    return {
        "session_id": session_id,
        "livekit_token": token,
        "livekit_url": livekit_url,
        "agent_name": agent_name
    }

@app.get("/api/session/{session_id}/status")
async def get_session_status(session_id: str):
    """Get status of an active session"""
    # For MVP, return mock status
    return {
        "session_id": session_id,
        "status": "active",
        "duration_seconds": 0,
        "messages_exchanged": 0
    }

@app.post("/api/session/{session_id}/end")
async def end_session(session_id: str):
    """End a tutoring session"""
    return {
        "session_id": session_id,
        "status": "ended",
        "message": "Session ended successfully"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

