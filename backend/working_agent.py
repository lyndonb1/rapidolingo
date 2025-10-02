"""
RápidoLingo Voice Agent - WORKING VERSION
Uses correct LiveKit voice.Agent API
"""

import os
import logging
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli
from livekit.agents import voice
from livekit.plugins import openai, silero, cartesia

# Import configuration
try:
    import config
    print("[✓] Config loaded")
except ImportError:
    print("[!] Using env vars")

# Validate
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")
CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")

if not CEREBRAS_API_KEY or not CARTESIA_API_KEY:
    raise ValueError("❌ API keys not set!")

print(f"[✓] Cerebras: {CEREBRAS_API_KEY[:15]}...")
print(f"[✓] Cartesia: {CARTESIA_API_KEY[:15]}...")

# Set for OpenAI compat
os.environ["OPENAI_API_KEY"] = CEREBRAS_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rapidolingo")


async def entrypoint(ctx: JobContext):
    """Entry point - called when participant joins"""
    logger.info(f"🎤 Joining room: {ctx.room.name}")
    
    # Connect
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    logger.info(f"✓ Connected to: {ctx.room.name}")

    # Create voice agent
    try:
        agent = voice.Agent(
            vad=silero.VAD.load(),
            stt=cartesia.STT(),
            llm=openai.LLM(
                base_url="https://api.cerebras.ai/v1",
                model="llama3.3-70b",
                temperature=0.7,
            ),
            tts=cartesia.TTS(
                voice="79a125e8-cd45-4c13-8a67-188112f4dd22"
            ),
            chat_ctx=voice.ChatCLI().make_chat_ctx(
                system_message=(
                    "You are María, a friendly Spanish restaurant server. "
                    "Help English speakers learn Spanish by mixing both languages naturally. "
                    "Keep responses SHORT - 1-2 sentences max. Be patient and encouraging."
                )
            ),
        )
        
        logger.info("✓ Voice agent created")
        
        # Start the agent
        agent.start(ctx.room)
        logger.info("✓ Agent started and listening!")
        
        # Initial greeting
        await agent.say(
            "¡Hola! Bienvenidos! Welcome to our restaurant. "
            "I'm María. What would you like to order?",
            allow_interruptions=True
        )
        
        logger.info("✓ Greeting sent - ready for conversation! 🎉")
        
    except Exception as e:
        logger.error(f"❌ Failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 RápidoLingo Voice Agent - Starting...")
    print("=" * 60)
    
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
        ),
    )

