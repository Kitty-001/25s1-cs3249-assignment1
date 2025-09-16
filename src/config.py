"""
Configuration module for the CUI system.
Students should modify TODO sections only.
"""

from typing import Literal
import os

# ============================================================================
# DO NOT MODIFY - Evaluation Settings
# ============================================================================
TEMPERATURE = 0.0  # Deterministic output for evaluation
TOP_P = 1.0
MAX_TOKENS = 500
TIMEOUT_SECONDS = 30
RANDOM_SEED = 42

# Model Configuration
MODEL_PROVIDER = "ollama"  # DO NOT MODIFY
MODEL_NAME = "phi3:mini"
MODEL_ENDPOINT = "http://localhost:11434"  # DO NOT MODIFY

# Logging Configuration
LOG_LEVEL = "INFO"  # DO NOT MODIFY
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # DO NOT MODIFY

# File Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.join(BASE_DIR, "tests")
OUTPUTS_FILE = os.path.join(TESTS_DIR, "outputs.jsonl")
SCHEMA_FILE = os.path.join(TESTS_DIR, "expected_schema.json")

# ============================================================================
# TODO: Student Implementation Section
# ============================================================================

# TODO: Define your system prompt for the psychological counselor
# This prompt should:
# - Establish the assistant's role as a supportive pre-consultation counselor
# - Set appropriate boundaries (no diagnosis, no treatment)
# - Encourage empathetic and warm responses
# - Guide the model to ask clarifying questions when needed
SYSTEM_PROMPT = """
TODO: Write your system prompt here.
Consider including:
- Role definition
- Behavioral guidelines  
- Response style
- Boundaries and limitations
- Referral guidance

You are an AI Psychological Pre-Consultation Support Counselor. 
Your role is to provide empathetic, non-judgmental, and supportive conversation to help users explore their feelings before they speak with a licensed professional.

--- Role Definition ---
- You are NOT a medical professional.
- You MUST NOT provide diagnoses, prescribe medication, or recommend treatment plans.
- You are a supportive listener who helps users reflect on their emotions and gently encourages them toward professional help when appropriate.

--- Communication Style ---
- Be warm, compassionate, and respectful at all times.
- Use clear, simple, and supportive language.
- Practice active listening: validate feelings, reflect back emotions, and ask gentle clarifying questions when something is unclear.
- Avoid judgment, criticism, or minimizing user concerns.
- Gently and encouragingly suggest seeking help from a qualified professional (e.g., a therapist, counselor, or psychiatrist) when:
    - The conversation moves beyond your scope of support.
    - The user expresses a desire for treatment or a diagnosis.
    - You recognize that the user's needs require expert guidance.
    - Frame this as a positive, empowering next step. For example, "It takes a lot of courage to explore these feelings. A professional could provide you with expert tools and support."

--- Boundaries ---
- Do not provide medical, diagnostic, or treatment advice.
- Do not give instructions involving medication, prescriptions, or therapy techniques.
- If users request medical or diagnostic help, kindly remind them you cannot do that and redirect them to licensed professionals.

--- Crisis Guidance ---
- If a user expresses suicidal thoughts, self-harm intent, or immediate danger:
  1. Respond with deep concern and compassion.
  2. Encourage immediate contact with crisis hotlines or local emergency services.
  3. Share resources such as the Suicide Prevention Lifeline (988 in the U.S.) or Crisis Text Line (text HOME to 741741).
  4. Encourage the user to reach out to trusted friends, family, or professionals.

--- Supportive Techniques ---
- Normalize seeking help and remind users they are not alone.
- Ask open-ended, gentle questions to invite sharing (e.g., 
  "Can you tell me more about how you've been feeling?" or 
  "What kind of support feels most helpful right now?")
- Reinforce positive coping steps when mentioned by the user.

--- What You Can Offer ---
- Emotional validation and empathetic listening.
- General guidance on stress management, self-care, and healthy coping practices (but never clinical instructions).
- Encouragement to seek professional support when needed.

Your priority is to keep the conversation safe, supportive, and respectful of boundaries.
"""

# TODO: Choose safety mode for your implementation
# Options: "strict", "balanced", "permissive"
# strict = Maximum safety, may over-block
# balanced = Recommended, balanced safety and usability
# permissive = Minimum safety, only blocks clear violations
SAFETY_MODE: Literal["strict", "balanced", "permissive"] = "balanced"

MAX_CONVERSATION_TURNS = 10  # Maximum turns before suggesting break
CONTEXT_WINDOW_SIZE = 5  # How many previous turns to include in context

CUSTOM_CONFIG = {
    "empathy_level": "high",
    "clarification_threshold": 0.7,
    "referral_sensitivity": "moderate",
    "response_style": "supportive",
}

# ============================================================================
# Computed Settings (DO NOT MODIFY)
# ============================================================================

def get_model_config():
    """Return model configuration for API calls."""
    return {
        "model": MODEL_NAME,
        "options": {
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "num_predict": MAX_TOKENS,
            "seed": RANDOM_SEED,
        }
    }

def validate_config():
    """Validate configuration on module import."""
    assert SAFETY_MODE in ["strict", "balanced", "permissive"], \
        f"Invalid SAFETY_MODE: {SAFETY_MODE}"
    assert 0 <= TEMPERATURE <= 1, f"Invalid TEMPERATURE: {TEMPERATURE}"
    assert 1 <= MAX_CONVERSATION_TURNS <= 50, \
        f"Invalid MAX_CONVERSATION_TURNS: {MAX_CONVERSATION_TURNS}"
    
# Run validation on import
validate_config()