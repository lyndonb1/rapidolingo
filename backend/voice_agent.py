"""
RápidoLingo Voice Agent - Simplified Working Version
Uses LiveKit agents framework with Cerebras + Cartesia
"""

import logging
import os
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import AssistantContext
from livekit.plugins import openai, silero, cartesia

# Import configuration
try:
    import config
    print("[✓] Configuration loaded")
except ImportError:
    print("[!] Config.py not found, using environment variables")

# Validate environment
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")
CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")

if not CEREBRAS_API_KEY:
    raise ValueError("❌ CEREBRAS_API_KEY not set!")
if not CARTESIA_API_KEY:
    raise ValueError("❌ CARTESIA_API_KEY not set!")

print(f"[✓] Cerebras API: {CEREBRAS_API_KEY[:15]}...")
print(f"[✓] Cartesia API: {CARTESIA_API_KEY[:15]}...")

# Set OpenAI API key for Cerebras compatibility
os.environ["OPENAI_API_KEY"] = CEREBRAS_API_KEY

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rapidolingo-agent")


async def entrypoint(ctx: JobContext):
    """
    Main entry point - called when a participant joins a room
    """
    logger.info(f"🎤 Agent joining room: {ctx.room.name}")
    
    # Initial instructions for the AI tutor
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are María, a friendly Spanish restaurant server helping English speakers learn Spanish. "
            "Mix Spanish and English in your responses. Teach vocabulary naturally while taking their order. "
            "Keep responses SHORT - 1-2 sentences max. Be encouraging and patient. "
            "Example: '¡Hola! Welcome! Would you like to ver el menú - see the menu?'"
        ),
    )

    # Connect to the room
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    logger.info(f"✓ Connected to room: {ctx.room.name}")

    # Create the assistant with all components
    try:
        logger.info("Creating voice assistant...")
        
        assistant = AssistantContext(
            llm=openai.LLM(
                base_url="https://api.cerebras.ai/v1",
                model="llama3.3-70b",
                temperature=0.7,
            ),
            tts=cartesia.TTS(
                voice="79a125e8-cd45-4c13-8a67-188112f4dd22"  # Female English voice
            ),
            vad=silero.VAD.load(),
            chat_ctx=initial_ctx,
        )
        
        logger.info("✓ Assistant created successfully")
        
        # Start the assistant
        assistant.start(ctx.room)
        logger.info("✓ Assistant started and listening")
        
        # Send initial greeting
        await assistant.say(
            "¡Hola! Bienvenidos! Welcome to our restaurant. I'm María. "
            "What would you like to order today?",
            allow_interruptions=True
        )
        
        logger.info("✓ Greeting sent - ready for conversation!")
        
    except Exception as e:
        logger.error(f"❌ Failed to start assistant: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 RápidoLingo Voice Agent Starting...")
    print("=" * 60)
    
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
        ),
    )

