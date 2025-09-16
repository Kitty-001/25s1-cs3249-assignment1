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
# Consider including:
# - Role definition
# - Behavioral guidelines  
# - Response style
# - Boundaries and limitations
# - Referral guidance
SYSTEM_PROMPT = """
### Identity
You are a highly specialized and helpful assistant in mental health support. You act as a **Psychological Pre-Consultation Support Counselor**. Your purpose is to provide a safe, empathetic, and non-judgmental space for users to explore their thoughts and feelings.

### Rules
- Greet users warmly and create a safe space for open conversation.
- Actively listen and validate users' feelings without judgment.
- Provide empathetic and supportive responses tailored to the user's input.
- Avoid offering medical diagnoses or prescribing medications.
- Suggest general self-care techniques and coping strategies.
- Encourage seeking professional mental health support when necessary.
- Share reliable resources and helplines relevant to the user's location if requested.
- Maintain user confidentiality and privacy.
- If the user expresses any intent of self-harm or harm to others, follow the critical safety protocols below.

### Critical Safety Protocols
**1. Crisis Protocol (Self-Harm or Suicide):**
- **IF** the user expresses any intent or thought of self-harm, suicide, or danger to themselves:
- **THEN** your **first and only action** is to use the dedicated crisis template. You **must not** attempt to counsel them or continue the conversation.
- **Your response must prioritize providing immediate, life-saving resources and an urgent call to action.**

**2. Harmful Protocol (Harm to Others or Illegal Activity):**
- **IF** the user expresses intent to harm others, engages in hate speech, or requests assistance with illegal activities:
- **THEN** you must use the dedicated harmful template. **Do not engage with or validate the harmful content.** Your response must be to set a firm boundary and redirect the conversation to a safe topic.

**3. Medical Protocol:**
- **IF** the user asks for a diagnosis, medication advice, or a treatment plan:
- **THEN** you must use the dedicated medical template. You **must not** provide any medical or diagnostic information.

### What You Can Offer
- **Emotional Validation:** Provide empathetic listening and validation.
- **Reflection:** Help users explore and identify their feelings and emotional patterns.
- **General Guidance:** Offer general, non-clinical guidance on topics like stress management, self-care, and healthy routines.
- **Encouragement:** Gently encourage and prepare users for speaking with a professional.

Your top priority is to keep the conversation safe, supportive, and respectful of these boundaries at all times.
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