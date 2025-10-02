"""
Simple LiveKit Agent for RápidoLingo
Single working agent using Cerebras + Cartesia
"""

import asyncio
import os
from pathlib import Path
from typing import Annotated

from livekit import agents, rtc
from livekit.agents import JobContext, WorkerOptions, cli, tokenize, tts
from livekit.agents.llm import (
    ChatContext,
    ChatImage,
    ChatMessage,
)
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero, cartesia as cartesia_plugin

# Import configuration
try:
    import config
    print("[INFO] Configuration loaded successfully")
except ImportError:
    print("[WARNING] config.py not found, using environment variables")

# Validate environment
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")
CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")
LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")

if not CEREBRAS_API_KEY:
    raise ValueError("CEREBRAS_API_KEY not set!")
if not CARTESIA_API_KEY:
    raise ValueError("CARTESIA_API_KEY not set!")
if not LIVEKIT_URL:
    raise ValueError("LIVEKIT_URL not set!")

print(f"[INFO] Cerebras API Key: {CEREBRAS_API_KEY[:20]}...")
print(f"[INFO] Cartesia API Key: {CARTESIA_API_KEY[:20]}...")
print(f"[INFO] LiveKit URL: {LIVEKIT_URL}")

# Set OpenAI API key for Cerebras
os.environ["OPENAI_API_KEY"] = CEREBRAS_API_KEY


async def entrypoint(ctx: JobContext):
    """
    Entry point for LiveKit agent worker
    This function is called when a participant joins a room
    """
    print(f"[AGENT] Starting agent for room: {ctx.room.name}")
    
    # Initial context - Spanish tutor personality
    initial_ctx = ChatContext().append(
        role="system",
        text=(
            "You are María, a friendly Spanish restaurant server. "
            "You help English speakers learn Spanish by having natural conversations about ordering food. "
            "Always respond in a mix of Spanish and English, teaching vocabulary as you go. "
            "Be patient, encouraging, and fun. Keep responses short (1-2 sentences max). "
            "Use simple Spanish phrases suitable for beginners."
        ),
    )

    # Connect to the room
    await ctx.connect()
    print(f"[AGENT] Connected to room: {ctx.room.name}")

    # Create assistant with Cerebras LLM and Cartesia TTS/STT
    try:
        assistant = VoiceAssistant(
            vad=silero.VAD.load(),  # Voice Activity Detection
            stt=cartesia_plugin.STT(),  # Speech to Text (Cartesia)
            llm=openai.LLM(
                base_url="https://api.cerebras.ai/v1",
                model="llama3.3-70b",
                temperature=0.7,
            ),
            tts=cartesia_plugin.TTS(
                voice="79a125e8-cd45-4c13-8a67-188112f4dd22"  # Female voice
            ),
            chat_ctx=initial_ctx,
        )
        
        print("[AGENT] Voice assistant created successfully")
        
        # Start the assistant
        assistant.start(ctx.room)
        print("[AGENT] Assistant started and listening...")
        
        # Greeting message
        await assistant.say(
            "¡Hola! Welcome to our restaurant. I'm María, your server. "
            "What can I get for you today?",
            allow_interruptions=True
        )
        
        print("[AGENT] Greeting sent")
        
    except Exception as e:
        print(f"[ERROR] Failed to create/start assistant: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    print("[WORKER] Starting LiveKit agent worker...")
    print("[WORKER] This will connect to LiveKit Cloud and wait for rooms")
    
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
        ),
    )

