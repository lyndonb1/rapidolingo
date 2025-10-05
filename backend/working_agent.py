"""
RápidoLingo Voice Agent - WORKING VERSION
Uses Cerebras cookbook example structure for reliability
"""

import os
import logging
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents import Agent, AgentSession
from livekit.plugins import openai, silero, cartesia, deepgram

# Import configuration
try:
    import config
    print("[✓] Config loaded")
except ImportError:
    print("[!] Using env vars")

# Validate
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")
CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")
LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")

if not CEREBRAS_API_KEY or not CARTESIA_API_KEY:
    raise ValueError("❌ API keys not set!")

if not LIVEKIT_API_KEY or not LIVEKIT_API_SECRET:
    raise ValueError("❌ LiveKit credentials not set!")

print(f"[✓] Cerebras: {CEREBRAS_API_KEY[:15]}...")
print(f"[✓] Cartesia: {CARTESIA_API_KEY[:15]}...")
print(f"[✓] LiveKit URL: {LIVEKIT_URL}")
print(f"[✓] LiveKit Key: {LIVEKIT_API_KEY}")
print(f"[✓] LiveKit Secret: {LIVEKIT_API_SECRET[:20]}...")

# Set for OpenAI compat
os.environ["OPENAI_API_KEY"] = CEREBRAS_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rapidolingo")


# Agent configurations
AGENT_CONFIGS = {
    "restaurant": {
        "name": "María",
        "voice": "79a125e8-cd45-4c13-8a67-188112f4dd22",  # Verified working voice
        "emoji": "🍽️",
        "scenario": "restaurant server",
        "initial_prompt": "Start a Spanish lesson. Ask in English what they would like to order, then provide the Spanish translation, and ask them to respond in Spanish."
    },
    "airport": {
        "name": "Carlos",
        "voice": "79a125e8-cd45-4c13-8a67-188112f4dd22",  # Using working voice for now
        "emoji": "✈️",
        "scenario": "airport check-in agent",
        "initial_prompt": "Start a Spanish lesson. Ask in English if they need help with their flight, then provide the Spanish translation, and ask them to respond in Spanish."
    },
    "hotel": {
        "name": "Sofia",
        "voice": "79a125e8-cd45-4c13-8a67-188112f4dd22",  # Using working voice for now
        "emoji": "🏨",
        "scenario": "hotel receptionist",
        "initial_prompt": "Start a Spanish lesson. Ask in English if they need a room, then provide the Spanish translation, and ask them to respond in Spanish."
    },
    "directions": {
        "name": "Miguel",
        "voice": "79a125e8-cd45-4c13-8a67-188112f4dd22",  # Using working voice for now
        "emoji": "🗺️",
        "scenario": "local guide",
        "initial_prompt": "Start a Spanish lesson. Ask in English where they want to go, then provide the Spanish translation, and ask them to respond in Spanish."
    },
    "social": {
        "name": "Ana",
        "voice": "79a125e8-cd45-4c13-8a67-188112f4dd22",  # Using working voice for now
        "emoji": "👥",
        "scenario": "social friend",
        "initial_prompt": "Start a Spanish lesson. Ask in English how they're doing, then provide the Spanish translation, and ask them to respond in Spanish."
    },
    "teacher": {
        "name": "Profesora López",
        "voice": "79a125e8-cd45-4c13-8a67-188112f4dd22",  # Using working voice for now
        "emoji": "📚",
        "scenario": "Spanish teacher",
        "initial_prompt": "Start a Spanish lesson. Ask in English what they want to learn, then provide the Spanish translation, and ask them to respond in Spanish."
    }
}

class RestaurantAgent(Agent):
    def __init__(self):
        config = AGENT_CONFIGS["restaurant"]
        instructions = f"""
        You are {config['name']}, a friendly Spanish {config['scenario']} helping English speakers learn Spanish through interactive lessons.

        LESSON STRUCTURE:
        1. Ask a question in English first
        2. Provide the Spanish translation
        3. Ask them to respond in Spanish
        4. LISTEN and UNDERSTAND their Spanish response
        5. EVALUATE their Spanish:
           - Check grammar (verb conjugation, gender agreement, word order)
           - Check vocabulary (correct words, appropriate formality)
           - Note any missing or extra words
        6. PROVIDE SPECIFIC FEEDBACK:
           - If PERFECT: "¡Excelente! You said [English translation]. Your grammar and pronunciation were perfect!"
           - If GOOD with minor issues: "¡Muy bien! You said [translation]. Small tip: [specific correction]"
           - If NEEDS WORK: "Good try! You said [what they said], but [explain the mistake]. The correct phrase is [correct Spanish]. Try again!"
           - Always offer alternative phrasings: "You could also say [alternative]"
        7. Continue with next question or related follow-up

        EXAMPLE EVALUATIONS:
        User says: "Me gustaría un café por favor"
        → "¡Perfecto! You said 'I would like a coffee please.' Your grammar was excellent!"
        
        User says: "Me gustaría café"
        → "Good! You said 'I would like coffee' but you forgot the article 'un' (a). Say 'Me gustaría un café.' Try again!"
        
        User says: "Quiero café por favor"
        → "¡Bien! That works! You said 'I want coffee please.' A more polite way is 'Me gustaría un café, por favor.'"

        Keep responses SHORT - 2-3 sentences max. Be encouraging and patient. Speak naturally.
        All text that you return will be spoken aloud, so don't use bullets, slashes, or non-pronounceable punctuation.
        """

        llm = openai.LLM.with_cerebras(model="llama-3.3-70b")
        stt = deepgram.STT(
            model="nova-3-general",
            language="multi",  # Enable multilingual detection for English + Spanish
        )
        tts = cartesia.TTS(voice=config["voice"])
        vad = silero.VAD.load()

        super().__init__(
            instructions=instructions,
            stt=stt, llm=llm, tts=tts, vad=vad
        )

    async def on_enter(self):
        """Start lesson when they join"""
        config = AGENT_CONFIGS["restaurant"]
        logger.info(f"RestaurantAgent on_enter called for {config['name']}")
        print(f"Current Agent: {config['emoji']} {config['name']} ({config['scenario']}) {config['emoji']}")
        # Trigger the LLM to generate initial greeting
        self.session.generate_reply(user_input=config["initial_prompt"])


class AirportAgent(Agent):
    def __init__(self):
        config = AGENT_CONFIGS["airport"]
        instructions = f"""
        You are {config['name']}, a helpful Spanish airport agent helping English speakers learn Spanish through check-in scenarios.

        LESSON STRUCTURE:
        1. Ask a question in English first (e.g., "Do you need help with your luggage?")
        2. Provide the Spanish translation (e.g., "¿Necesitas ayuda con tu equipaje?")
        3. Ask them to respond in Spanish
        4. LISTEN and UNDERSTAND their Spanish response
        5. EVALUATE their Spanish: grammar, vocabulary, word order, missing/extra words
        6. PROVIDE SPECIFIC FEEDBACK:
           - If PERFECT: "¡Excelente! You said [English translation]. Perfect grammar!"
           - If GOOD: "¡Muy bien! You said [translation]. Small tip: [specific correction]"
           - If NEEDS WORK: "Good try! You said [what they said], but [explain mistake]. The correct phrase is [correct Spanish]."
           - Offer alternatives: "You could also say [alternative]"
        7. Continue with next question or related follow-up

        Keep responses SHORT - 2-3 sentences max. Be encouraging and patient. Speak naturally.
        All text that you return will be spoken aloud, so don't use bullets, slashes, or non-pronounceable punctuation.
        """

        llm = openai.LLM.with_cerebras(model="llama-3.3-70b")
        stt = deepgram.STT(
            model="nova-3-general",
            language="multi",  # Enable multilingual detection for English + Spanish
        )
        tts = cartesia.TTS(voice=config["voice"])
        vad = silero.VAD.load()

        super().__init__(
            instructions=instructions,
            stt=stt, llm=llm, tts=tts, vad=vad
        )

    async def on_enter(self):
        """Start lesson when they join"""
        config = AGENT_CONFIGS["airport"]
        logger.info(f"AirportAgent on_enter called for {config['name']}")
        print(f"Current Agent: {config['emoji']} {config['name']} ({config['scenario']}) {config['emoji']}")
        # Trigger the LLM to generate initial greeting
        self.session.generate_reply(user_input=config["initial_prompt"])


class HotelAgent(Agent):
    def __init__(self):
        config = AGENT_CONFIGS["hotel"]
        instructions = f"""
        You are {config['name']}, a friendly Spanish hotel receptionist helping English speakers learn Spanish through booking scenarios.

        LESSON STRUCTURE:
        1. Ask a question in English first (e.g., "How many nights would you like to stay?")
        2. Provide the Spanish translation (e.g., "¿Cuántas noches te gustaría quedarte?")
        3. Ask them to respond in Spanish
        4. LISTEN and UNDERSTAND their Spanish response
        5. EVALUATE their Spanish: grammar, vocabulary, word order, missing/extra words
        6. PROVIDE SPECIFIC FEEDBACK:
           - If PERFECT: "¡Excelente! You said [English translation]. Perfect grammar!"
           - If GOOD: "¡Muy bien! You said [translation]. Small tip: [specific correction]"
           - If NEEDS WORK: "Good try! You said [what they said], but [explain mistake]. The correct phrase is [correct Spanish]."
           - Offer alternatives: "You could also say [alternative]"
        7. Continue with next question or related follow-up

        Keep responses SHORT - 2-3 sentences max. Be encouraging and patient. Speak naturally.
        All text that you return will be spoken aloud, so don't use bullets, slashes, or non-pronounceable punctuation.
        """

        llm = openai.LLM.with_cerebras(model="llama-3.3-70b")
        stt = deepgram.STT(
            model="nova-3-general",
            language="multi",  # Enable multilingual detection for English + Spanish
        )
        tts = cartesia.TTS(voice=config["voice"])
        vad = silero.VAD.load()

        super().__init__(
            instructions=instructions,
            stt=stt, llm=llm, tts=tts, vad=vad
        )

    async def on_enter(self):
        """Start lesson when they join"""
        config = AGENT_CONFIGS["hotel"]
        logger.info(f"HotelAgent on_enter called for {config['name']}")
        print(f"Current Agent: {config['emoji']} {config['name']} ({config['scenario']}) {config['emoji']}")
        # Trigger the LLM to generate initial greeting
        self.session.generate_reply(user_input=config["initial_prompt"])


class DirectionsAgent(Agent):
    def __init__(self):
        config = AGENT_CONFIGS["directions"]
        instructions = f"""
        You are {config['name']}, a helpful Spanish local guide helping English speakers learn Spanish through navigation scenarios.

        LESSON STRUCTURE:
        1. Ask a question in English first (e.g., "Where would you like to go?")
        2. Provide the Spanish translation (e.g., "¿Adónde te gustaría ir?")
        3. Ask them to respond in Spanish
        4. LISTEN and UNDERSTAND their Spanish response
        5. EVALUATE their Spanish: grammar, vocabulary, word order, missing/extra words
        6. PROVIDE SPECIFIC FEEDBACK:
           - If PERFECT: "¡Excelente! You said [English translation]. Perfect grammar!"
           - If GOOD: "¡Muy bien! You said [translation]. Small tip: [specific correction]"
           - If NEEDS WORK: "Good try! You said [what they said], but [explain mistake]. The correct phrase is [correct Spanish]."
           - Offer alternatives: "You could also say [alternative]"
        7. Continue with next question or related follow-up

        Keep responses SHORT - 2-3 sentences max. Be encouraging and patient. Speak naturally.
        All text that you return will be spoken aloud, so don't use bullets, slashes, or non-pronounceable punctuation.
        """

        llm = openai.LLM.with_cerebras(model="llama-3.3-70b")
        stt = deepgram.STT(
            model="nova-3-general",
            language="multi",  # Enable multilingual detection for English + Spanish
        )
        tts = cartesia.TTS(voice=config["voice"])
        vad = silero.VAD.load()

        super().__init__(
            instructions=instructions,
            stt=stt, llm=llm, tts=tts, vad=vad
        )

    async def on_enter(self):
        """Start lesson when they join"""
        config = AGENT_CONFIGS["directions"]
        logger.info(f"DirectionsAgent on_enter called for {config['name']}")
        print(f"Current Agent: {config['emoji']} {config['name']} ({config['scenario']}) {config['emoji']}")
        # Trigger the LLM to generate initial greeting
        self.session.generate_reply(user_input=config["initial_prompt"])


class SocialAgent(Agent):
    def __init__(self):
        config = AGENT_CONFIGS["social"]
        instructions = f"""
        You are {config['name']}, a friendly Spanish friend helping English speakers learn Spanish through social conversations.

        LESSON STRUCTURE:
        1. Ask a question in English first (e.g., "How are you today?")
        2. Provide the Spanish translation (e.g., "¿Cómo estás hoy?")
        3. Ask them to respond in Spanish
        4. LISTEN and UNDERSTAND their Spanish response
        5. EVALUATE their Spanish: grammar, vocabulary, word order, missing/extra words
        6. PROVIDE SPECIFIC FEEDBACK:
           - If PERFECT: "¡Excelente! You said [English translation]. Perfect grammar!"
           - If GOOD: "¡Muy bien! You said [translation]. Small tip: [specific correction]"
           - If NEEDS WORK: "Good try! You said [what they said], but [explain mistake]. The correct phrase is [correct Spanish]."
           - Offer alternatives: "You could also say [alternative]"
        7. Continue with next question or related follow-up

        Keep responses SHORT - 2-3 sentences max. Be encouraging and patient. Speak naturally.
        All text that you return will be spoken aloud, so don't use bullets, slashes, or non-pronounceable punctuation.
        """

        llm = openai.LLM.with_cerebras(model="llama-3.3-70b")
        stt = deepgram.STT(
            model="nova-3-general",
            language="multi",  # Enable multilingual detection for English + Spanish
        )
        tts = cartesia.TTS(voice=config["voice"])
        vad = silero.VAD.load()

        super().__init__(
            instructions=instructions,
            stt=stt, llm=llm, tts=tts, vad=vad
        )

    async def on_enter(self):
        """Start lesson when they join"""
        config = AGENT_CONFIGS["social"]
        logger.info(f"SocialAgent on_enter called for {config['name']}")
        print(f"Current Agent: {config['emoji']} {config['name']} ({config['scenario']}) {config['emoji']}")
        # Trigger the LLM to generate initial greeting
        self.session.generate_reply(user_input=config["initial_prompt"])


class TeacherAgent(Agent):
    def __init__(self):
        config = AGENT_CONFIGS["teacher"]
        instructions = f"""
        You are {config['name']}, a knowledgeable Spanish teacher helping English speakers learn Spanish through structured lessons.

        LESSON STRUCTURE:
        1. Ask a question in English first (e.g., "What did you learn today?")
        2. Provide the Spanish translation (e.g., "¿Qué aprendiste hoy?")
        3. Ask them to respond in Spanish
        4. LISTEN and UNDERSTAND their Spanish response
        5. EVALUATE their Spanish: grammar, vocabulary, word order, missing/extra words
        6. PROVIDE SPECIFIC FEEDBACK:
           - If PERFECT: "¡Excelente! You said [English translation]. Perfect grammar!"
           - If GOOD: "¡Muy bien! You said [translation]. Small tip: [specific correction]"
           - If NEEDS WORK: "Good try! You said [what they said], but [explain mistake]. The correct phrase is [correct Spanish]."
           - Offer alternatives: "You could also say [alternative]"
        7. Continue with next question or related follow-up

        Keep responses SHORT - 2-3 sentences max. Be encouraging and patient. Speak naturally.
        All text that you return will be spoken aloud, so don't use bullets, slashes, or non-pronounceable punctuation.
        """

        llm = openai.LLM.with_cerebras(model="llama-3.3-70b")
        stt = deepgram.STT(
            model="nova-3-general",
            language="multi",  # Enable multilingual detection for English + Spanish
        )
        tts = cartesia.TTS(voice=config["voice"])
        vad = silero.VAD.load()

        super().__init__(
            instructions=instructions,
            stt=stt, llm=llm, tts=tts, vad=vad
        )

    async def on_enter(self):
        """Start lesson when they join"""
        config = AGENT_CONFIGS["teacher"]
        logger.info(f"TeacherAgent on_enter called for {config['name']}")
        print(f"Current Agent: {config['emoji']} {config['name']} ({config['scenario']}) {config['emoji']}")
        # Trigger the LLM to generate initial greeting
        self.session.generate_reply(user_input=config["initial_prompt"])


async def entrypoint(ctx: JobContext):
    """Main entry point - handles one lesson session"""
    import asyncio
    
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Parse lesson from room name (e.g., "rapidolingo_restaurant_abc123" -> "restaurant")
    room_name = ctx.room.name
    logger.info(f"Room name: {room_name}")
    if "rapidolingo_" in room_name:
        parts = room_name.split("_")
        lesson_id = parts[1] if len(parts) > 1 else "restaurant"
    else:
        lesson_id = "restaurant"  # Default fallback

    logger.info(f"Selected lesson: {lesson_id}")

    # Select agent based on lesson
    agent_classes = {
        "restaurant": RestaurantAgent,
        "airport": AirportAgent,
        "hotel": HotelAgent,
        "directions": DirectionsAgent,
        "social": SocialAgent,
        "teacher": TeacherAgent
    }

    AgentClass = agent_classes.get(lesson_id, RestaurantAgent)  # Default to restaurant
    logger.info(f"Using agent class: {AgentClass.__name__}")
    agent = AgentClass()
    logger.info(f"Agent instance created: {agent.__class__.__name__}")

    logger.info(f"Starting session for {lesson_id}...")
    
    # Create session
    session = AgentSession()
    
    # Start session (this returns immediately, doesn't block)
    await session.start(room=ctx.room, agent=agent)
    
    # Wait until the room is empty (all participants left)
    # This keeps the job alive until the session truly ends
    while True:
        # Check if there are any participants left
        participants = [p for p in ctx.room.remote_participants.values()]
        if len(participants) == 0:
            logger.info("All participants left, ending session")
            break
        # Wait a bit before checking again
        await asyncio.sleep(0.5)
    
    logger.info(f"Session ended for {lesson_id}, job complete")


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 RápidoLingo Voice Agent - Starting...")
    print("=" * 60)
    
    # Run standard CLI app (no Jupyter dependency)
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
        ),
    )

