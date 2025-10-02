import os
import json
from openai import OpenAI

# Configure Cerebras API
CEREBRAS_API_KEY = "csk-eryjc8myc6xjh6tex3fyfp8e9pvyjnmknxtpxcpc9cvftwvd"

client = OpenAI(
    api_key=CEREBRAS_API_KEY,
    base_url="https://api.cerebras.ai/v1"
)

def generate_content(prompt, filename):
    """Generate content using Cerebras and save to JSON"""
    print(f"Generating {filename}...")
    
    response = client.chat.completions.create(
        model="llama-3.3-70b",
        messages=[
            {"role": "system", "content": "You are an expert Spanish language teacher. Generate high-quality educational content in valid JSON format."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=4000
    )
    
    content = response.choices[0].message.content
    
    # Save to file
    with open(f"context/{filename}", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ {filename} created!")
    return content

# Generate beginner phrases
beginner_prompt = """
Create a JSON file with 50 essential Spanish phrases for absolute beginners.
Include: greetings, introductions, basic questions, common responses, polite expressions.

Format:
{
  "beginner_phrases": [
    {
      "spanish": "Hola, ¿cómo estás?",
      "english": "Hello, how are you?",
      "pronunciation": "OH-lah, KOH-moh es-TAHS",
      "category": "greetings",
      "difficulty": "beginner"
    }
  ]
}

Return ONLY valid JSON, no markdown formatting.
"""

# Generate conversation scenarios
scenarios_prompt = """
Create realistic Spanish conversation scenarios for language learners.
Include: restaurant, airport, hotel, shopping, asking directions.

Format:
{
  "scenarios": [
    {
      "title": "Ordering at a Restaurant",
      "difficulty": "beginner",
      "dialogue": [
        {"speaker": "waiter", "spanish": "Buenas tardes. ¿Qué desea?", "english": "Good afternoon. What would you like?"},
        {"speaker": "customer", "spanish": "Una mesa para dos, por favor.", "english": "A table for two, please."}
      ],
      "vocabulary": ["mesa", "por favor", "desea"],
      "tips": "Always use 'por favor' to be polite"
    }
  ]
}

Create 5 scenarios. Return ONLY valid JSON, no markdown.
"""

# Generate vocabulary lists
vocab_prompt = """
Create Spanish vocabulary lists organized by difficulty level.
Include: beginner (100 words), intermediate (50 words), advanced (30 words).
Focus on most commonly used words.

Format:
{
  "vocabulary": {
    "beginner": [
      {"spanish": "agua", "english": "water", "pronunciation": "AH-gwah", "category": "food"},
      {"spanish": "casa", "english": "house", "pronunciation": "KAH-sah", "category": "places"}
    ],
    "intermediate": [],
    "advanced": []
  }
}

Return ONLY valid JSON, no markdown.
"""

# Generate grammar rules
grammar_prompt = """
Create essential Spanish grammar rules for beginners and intermediate learners.
Include: verb conjugations, gender rules, articles, common patterns.

Format:
{
  "grammar_rules": [
    {
      "topic": "Present Tense AR Verbs",
      "level": "beginner",
      "explanation": "AR verbs like hablar (to speak) conjugate by removing -ar and adding endings",
      "examples": [
        {"spanish": "Yo hablo", "english": "I speak"},
        {"spanish": "Tú hablas", "english": "You speak"}
      ],
      "common_verbs": ["hablar", "caminar", "estudiar"]
    }
  ]
}

Create 8 grammar rules covering basics. Return ONLY valid JSON, no markdown.
"""

# Generate pronunciation guide
pronunciation_prompt = """
Create a Spanish pronunciation guide for English speakers.
Cover: vowels, consonants, special characters (ñ, ll, rr), stress patterns.

Format:
{
  "pronunciation_guide": [
    {
      "letter": "a",
      "sound": "ah",
      "description": "Always pronounced like 'a' in 'father'",
      "examples": ["casa (KAH-sah)", "mama (MAH-mah)"]
    }
  ]
}

Return ONLY valid JSON, no markdown.
"""

if __name__ == "__main__":
    print("🚀 Generating Spanish learning content with Cerebras...")
    print("=" * 60)
    
    # Generate all content files
    generate_content(beginner_prompt, "spanish_beginner.json")
    generate_content(scenarios_prompt, "spanish_scenarios.json")
    generate_content(vocab_prompt, "spanish_vocabulary.json")
    generate_content(grammar_prompt, "spanish_grammar.json")
    generate_content(pronunciation_prompt, "spanish_pronunciation.json")
    
    print("=" * 60)
    print("✅ All Spanish learning content generated!")
    print("📁 Files saved to context/ directory")
    print("⚡ Powered by Cerebras LLaMA 3.3 70B")

