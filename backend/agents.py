"""
RápidoLingo Multi-Agent System
6 specialized agents for Spanish tutoring scenarios
"""

import os
import json
from pathlib import Path
from livekit.agents import Agent, function_tool
from livekit.plugins import openai, silero, cartesia

# Import configuration first
try:
    import config
except ImportError:
    # Fallback if config.py not found
    pass

# Load Spanish content once
CONTEXT_DIR = Path("../context")

def load_context():
    """Load all Spanish learning content"""
    all_content = ""
    for json_file in CONTEXT_DIR.glob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            content = f.read()
            all_content += f"\n=== {json_file.stem} ===\n{content}\n"
    return all_content

SPANISH_CONTENT = load_context()

# Base configuration - get from environment (set by config.py)
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")
CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")

# Validate API keys
if not CEREBRAS_API_KEY:
    raise ValueError("CEREBRAS_API_KEY not found in environment. Make sure config.py is imported.")
if not CARTESIA_API_KEY:
    raise ValueError("CARTESIA_API_KEY not found in environment. Make sure config.py is imported.")

os.environ["OPENAI_API_KEY"] = CEREBRAS_API_KEY  # For LiveKit OpenAI plugin

#===============================================================================
# TEACHER AGENT - Main Coordinator
#===============================================================================

class TeacherAgent(Agent):
    """
    Main Spanish teacher - coordinates learning and transfers to specialists
    """
    def __init__(self):
        llm = openai.LLM.with_cerebras(
            model="llama-3.3-70b",
            base_url="https://api.cerebras.ai/v1"
        )
        stt = cartesia.STT()
        tts = cartesia.TTS(voice="79a125e8-cd45-4c13-8a67-188112f4dd22")  # Default female voice
        vad = silero.VAD.load()

        instructions = f"""
        You are Profesora López, a friendly and encouraging Spanish teacher.
        Speak naturally and clearly. All responses will be spoken aloud.
        
        Your role:
        - Welcome students and assess their level
        - Suggest appropriate scenarios to practice
        - Provide pronunciation feedback
        - Transfer to specialized agents for scenarios
        - Give encouragement and learning tips
        
        You have access to this Spanish learning content:
        {SPANISH_CONTENT}
        
        CRITICAL RULES:
        - Speak in English when explaining concepts
        - Use Spanish for examples and demonstrations
        - Be patient and encouraging
        - If student wants to practice a scenario, transfer to the appropriate agent
        - Keep responses conversational and natural (no bullets or lists)
        """

        super().__init__(
            instructions=instructions,
            stt=stt, llm=llm, tts=tts, vad=vad
        )

    async def on_enter(self):
        print("Current Agent: 📚 Teacher Agent (Profesora López) 📚")
        self.session.generate_reply(
            user_input="Greet the student warmly in English. Introduce yourself as Profesora López. Ask what they'd like to practice today."
        )

    @function_tool
    async def transfer_to_restaurant(self):
        """Transfer to restaurant agent for dining scenario practice"""
        await self.session.generate_reply(
            user_input="Tell the student you're transferring them to the restaurant scenario. Wish them luck!"
        )
        return RestaurantAgent()

    @function_tool
    async def transfer_to_airport(self):
        """Transfer to airport agent for travel scenario practice"""
        await self.session.generate_reply(
            user_input="Tell student you're transferring them to the airport scenario."
        )
        return AirportAgent()

    @function_tool
    async def transfer_to_hotel(self):
        """Transfer to hotel agent for accommodation scenario practice"""
        await self.session.generate_reply(
            user_input="Tell student you're transferring them to the hotel scenario."
        )
        return HotelAgent()

    @function_tool
    async def transfer_to_directions(self):
        """Transfer to directions agent for navigation practice"""
        await self.session.generate_reply(
            user_input="Tell student you're transferring them to directions practice."
        )
        return DirectionsAgent()

    @function_tool
    async def transfer_to_social(self):
        """Transfer to social agent for casual conversation practice"""
        await self.session.generate_reply(
            user_input="Tell student you're transferring them to social conversation practice."
        )
        return SocialAgent()

#===============================================================================
# RESTAURANT AGENT - Waiter/Server
#===============================================================================

class RestaurantAgent(Agent):
    """
    Restaurant waiter - practices ordering food, asking for menu items
    """
    def __init__(self):
        llm = openai.LLM.with_cerebras(
            model="llama-3.3-70b",
            base_url="https://api.cerebras.ai/v1"
        )
        stt = cartesia.STT()
        tts = cartesia.TTS(voice="a0e99841-438c-4a64-b679-ae501e7d6091")  # Different voice for variety
        vad = silero.VAD.load()

        # Load restaurant scenario content
        restaurant_content = ""
        try:
            with open(CONTEXT_DIR / "spanish_scenarios.json", 'r', encoding='utf-8') as f:
                scenarios = json.load(f)
                for scenario in scenarios.get("scenarios", []):
                    if "restaurant" in scenario.get("title", "").lower():
                        restaurant_content += json.dumps(scenario, indent=2)
        except:
            pass

        instructions = f"""
        You are María, a friendly Spanish restaurant server.
        Conduct the entire conversation IN SPANISH only.
        
        Scenario: You are serving at a Spanish restaurant. The customer (student) will practice ordering.
        
        Your role:
        - Greet the customer warmly in Spanish
        - Offer a table
        - Present menu options
        - Take orders
        - Suggest popular dishes
        - Bring the check when asked
        
        Restaurant context and phrases:
        {restaurant_content}
        
        IMPORTANT:
        - Speak ONLY in Spanish
        - Speak slowly and clearly
        - If student struggles, repeat slowly
        - Be encouraging and patient
        - Use authentic restaurant vocabulary
        - No English unless student explicitly asks for translation
        """

        super().__init__(
            instructions=instructions,
            stt=stt, llm=llm, tts=tts, vad=vad
        )

    async def on_enter(self):
        print("Current Agent: 🍽️ Restaurant Agent (María) 🍽️")
        await self.session.say("¡Buenas tardes! Bienvenido a nuestro restaurante. ¿Mesa para cuántas personas?")

    @function_tool
    async def return_to_teacher(self):
        """Return to main teacher agent"""
        await self.session.say("¡Muy bien! Has practicado muy bien. Regresando a la profesora López.")
        return TeacherAgent()

#===============================================================================
# AIRPORT AGENT - Airline Staff
#===============================================================================

class AirportAgent(Agent):
    """Airport check-in agent - practices travel scenarios"""
    def __init__(self):
        llm = openai.LLM.with_cerebras(
            model="llama-3.3-70b",
            base_url="https://api.cerebras.ai/v1"
        )
        stt = cartesia.STT()
        tts = cartesia.TTS(voice="248be419-c632-4f23-adf1-5324ed7dbf1d")  # Professional voice
        vad = silero.VAD.load()

        instructions = f"""
        You are Carlos, a professional airport check-in agent.
        Conduct conversation IN SPANISH only.
        
        Scenario: Airport check-in counter
        
        Your role:
        - Check passports
        - Ask about luggage
        - Issue boarding passes
        - Give gate information
        
        Use Spanish content: {SPANISH_CONTENT[:2000]}
        
        IMPORTANT:
        - Speak ONLY in Spanish
        - Use formal "usted" form
        - Be professional and efficient
        - Speak clearly for language learners
        """

        super().__init__(
            instructions=instructions,
            stt=stt, llm=llm, tts=tts, vad=vad
        )

    async def on_enter(self):
        print("Current Agent: ✈️ Airport Agent (Carlos) ✈️")
        await self.session.say("Buenos días. Su pasaporte, por favor.")

    @function_tool
    async def return_to_teacher(self):
        """Return to main teacher"""
        await self.session.say("¡Buen viaje! Regresando a la profesora.")
        return TeacherAgent()

#===============================================================================
# HOTEL AGENT - Receptionist
#===============================================================================

class HotelAgent(Agent):
    """Hotel receptionist - practices accommodation scenarios"""
    def __init__(self):
        llm = openai.LLM.with_cerebras(
            model="llama-3.3-70b",
            base_url="https://api.cerebras.ai/v1"
        )
        stt = cartesia.STT()
        tts = cartesia.TTS(voice="156fb8d2-335b-4950-9cb3-a2d33befec77")  # Friendly female voice
        vad = silero.VAD.load()

        instructions = f"""
        You are Sofia, a helpful hotel receptionist.
        Conduct conversation IN SPANISH only.
        
        Scenario: Hotel check-in desk
        
        Your role:
        - Welcome guests
        - Check reservations
        - Provide room numbers
        - Give information about amenities
        - Answer questions about breakfast, WiFi, etc.
        
        IMPORTANT:
        - Speak ONLY in Spanish
        - Use formal "usted" initially
        - Be welcoming and helpful
        - Speak clearly
        """

        super().__init__(
            instructions=instructions,
            stt=stt, llm=llm, tts=tts, vad=vad
        )

    async def on_enter(self):
        print("Current Agent: 🏨 Hotel Agent (Sofia) 🏨")
        await self.session.say("¡Bienvenido! ¿Tiene una reserva?")

    @function_tool
    async def return_to_teacher(self):
        """Return to teacher"""
        await self.session.say("¡Que disfrute su estancia! Regresando a la profesora.")
        return TeacherAgent()

#===============================================================================
# DIRECTIONS AGENT - Helpful Local
#===============================================================================

class DirectionsAgent(Agent):
    """Local helper - practices asking for and giving directions"""
    def __init__(self):
        llm = openai.LLM.with_cerebras(
            model="llama-3.3-70b",
            base_url="https://api.cerebras.ai/v1"
        )
        stt = cartesia.STT()
        tts = cartesia.TTS(voice="87748186-23bb-4158-a1eb-332911b0b708")  # Casual male voice
        vad = silero.VAD.load()

        instructions = f"""
        You are Miguel, a friendly local person helping tourists.
        Conduct conversation IN SPANISH only.
        
        Scenario: Tourist asks you for directions on the street
        
        Your role:
        - Help tourists find places
        - Give clear directions (left, right, straight)
        - Estimate walking time
        - Be friendly and helpful
        
        IMPORTANT:
        - Speak ONLY in Spanish
        - Use "tú" (informal) - you're being friendly
        - Be patient with tourists
        - Use directional vocabulary: derecha, izquierda, recto
        """

        super().__init__(
            instructions=instructions,
            stt=stt, llm=llm, tts=tts, vad=vad
        )

    async def on_enter(self):
        print("Current Agent: 🗺️ Directions Agent (Miguel) 🗺️")
        await self.session.say("Hola! Claro, te puedo ayudar. ¿Qué estás buscando?")

    @function_tool
    async def return_to_teacher(self):
        """Return to teacher"""
        await self.session.say("¡Buen viaje! Regresando a la profesora.")
        return TeacherAgent()

#===============================================================================
# SOCIAL AGENT - Conversation Partner
#===============================================================================

class SocialAgent(Agent):
    """Casual friend - practices social conversations"""
    def __init__(self):
        llm = openai.LLM.with_cerebras(
            model="llama-3.3-70b",
            base_url="https://api.cerebras.ai/v1"
        )
        stt = cartesia.STT()
        tts = cartesia.TTS(voice="2ee87190-8f84-4925-97da-e52547f9462c")  # Friendly voice
        vad = silero.VAD.load()

        instructions = f"""
        You are Ana, a friendly Spanish speaker looking to make friends.
        Conduct conversation IN SPANISH only.
        
        Scenario: Meeting someone new / casual social situation
        
        Your role:
        - Make small talk
        - Ask about hobbies, interests
        - Talk about weather, plans, movies
        - Be friendly and conversational
        - Make plans to meet up
        
        Social content: {SPANISH_CONTENT[:2000]}
        
        IMPORTANT:
        - Speak ONLY in Spanish
        - Use "tú" (informal/friendly)
        - Be warm and engaging
        - Ask follow-up questions
        - Keep conversation flowing naturally
        """

        super().__init__(
            instructions=instructions,
            stt=stt, llm=llm, tts=tts, vad=vad
        )

    async def on_enter(self):
        print("Current Agent: 👥 Social Agent (Ana) 👥")
        await self.session.say("¡Hola! ¿Qué tal? Me llamo Ana. ¿Cómo te llamas?")

    @function_tool
    async def return_to_teacher(self):
        """Return to teacher"""
        await self.session.say("¡Fue un placer conocerte! Regresando a la profesora.")
        return TeacherAgent()

