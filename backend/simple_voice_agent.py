"""
Simple Voice Agent - Minimal version for testing
"""
import os
import logging
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.plugins import openai, silero, cartesia

# Import configuration
try:
    import config
    print("[OK] Config loaded")
except ImportError:
    print("[!] Using env vars")

# Validate
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")
CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")

if not CEREBRAS_API_KEY or not CARTESIA_API_KEY:
    raise ValueError("API keys not set!")

print(f"[OK] Cerebras: {CEREBRAS_API_KEY[:15]}...")
print(f"[OK] Cartesia: {CARTESIA_API_KEY[:15]}...")

# Set for OpenAI compat
os.environ["OPENAI_API_KEY"] = CEREBRAS_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rapidolingo")


async def entrypoint(ctx: JobContext):
    """Simple entry point"""
    logger.info(f"Room: {ctx.room.name}")
    
    # Connect
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    logger.info("Connected!")

    # Wait for participant
    participant = await ctx.wait_for_participant()
    logger.info(f"Participant ready: {participant.identity}")

    # Initial context
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are María, a friendly Spanish restaurant server. "
            "Mix Spanish and English. Keep responses SHORT - 1-2 sentences max."
        ),
    )

    # Create assistant (simpler version)
    from livekit.agents.voice_assistant import VoiceAssistant
    
    assistant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=openai.STT(),  # Use OpenAI STT instead of Cartesia
        llm=openai.LLM(
            base_url="https://api.cerebras.ai/v1",
            model="llama3.3-70b",
            temperature=0.7,
        ),
        tts=cartesia.TTS(
            voice="79a125e8-cd45-4c13-8a67-188112f4dd22"
        ),
        chat_ctx=initial_ctx,
    )
    
    logger.info("Assistant created!")
    
    # Start
    assistant.start(ctx.room, participant)
    logger.info("Assistant started!")
    
    # Greeting
    await assistant.say(
        "Hola! Welcome to our restaurant. I'm María. What would you like?",
        allow_interruptions=True
    )
    
    logger.info("Ready!")


if __name__ == "__main__":
    print("=" * 60)
    print("Simple Voice Agent Starting...")
    print("=" * 60)
    
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
        ),
    )

