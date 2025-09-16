"""
Content moderation module for safety enforcement.
Students must complete TODO sections according to POLICY.md.
"""

import logging
import re
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple

from .config import SAFETY_MODE

logger = logging.getLogger(__name__)


class ModerationAction(Enum):
    """Possible moderation actions."""
    ALLOW = "allow"
    BLOCK = "block"
    SAFE_FALLBACK = "safe_fallback"


@dataclass
class ModerationResult:
    """Result of moderation check."""
    action: ModerationAction
    tags: List[str]  # Policy tags that were triggered
    reason: str  # Human-readable explanation
    confidence: float  # Confidence level (0-1)
    fallback_response: Optional[str] = None  # Response to use if action != ALLOW


class Moderator:
    """Handles content moderation according to safety policy."""
    
    def __init__(self):
        """Initialize the moderator with safety rules."""
        self.safety_mode = SAFETY_MODE
        self._initialize_rules()
    
    def _initialize_rules(self):
        """
        Initialize moderation rules based on POLICY.md.
        TODO: Students must define these based on their POLICY.md
        
        IMPLEMENTATION GUIDE:
        1. Copy all keywords and patterns from your completed POLICY.md
        2. Ensure Python formatting (lists, strings, regex compilation)
        3. Templates should be multi-line strings with proper formatting
        """
        
        # DONE: Define crisis keywords and patterns
        # These should detect immediate risk of harm
        self.crisis_keywords = [
            # Example (students should expand):
            # "suicide", "end my life"
            # DONE: Add comprehensive list
            # Direct suicide mentions (examples - add more keywords):
            "suicide", "su1cide", "sui-cide"
            "end my life", "kill myself", "kms",
            "want to die", "better off die"

            # Self-harm expressions (examples - add more keywords):
            "hurt myself", "self-harm", "gun",
            "shoot myself", "stab myself", "poison",
            "suffocate", "choke myself", "bury myself"
            
            # Imminent danger indicators (examples - add more keywords):
            "goodbye forever", "final message", "end it all",
            "disappear forever", "don't want to live",
            "want to sleep forever", "never wake up", 
            "nothing matters", "lost all purpose" 
        ]
        
        # DONE: Crisis patterns - regex for complex expressions
        self.crisis_patterns = [
            # Example regex patterns:
            r"\b(want|going|plan|ready) to (die|kill|hurt|end)\b",
            r"\b(thinking|thought) about (suicide|dying|ending it)\b",
            # r"\b(want|going|plan|ready) to (die|kill|hurt|end)\b",
            # DONE: Add patterns for crisis detection
            # Action / intent oriented (explicit)
            r"\b(want|wanna|wanna|wanna|wanna|wanna|wanting|planning|plan|going|gonna|ready)\s+(to|2)\s+(die|kill( myself)?|end( my life| it all)?|hurt( myself)?)\b",

            # Compact action forms and slang (kms, unalive)
            r"\b(kms|killme|kill myself|kill myself|unalive|off myself|offme|off myself)\b",
            r"\b(suicide|suicidal|suicid(al)?|su1cide|sucide|sui.cide)\b",

            # Specific methods / immediate danger indicators
            r"\b(shot myself|shoot myself|shooting myself|hang myself|hanging|take (too )?many pills|overdose|od|poison( myself|ing)?|drown myself|jump off( a)?\b)",
            r"\b((drive|crash) (the car|my car) (on purpose|into)|drive into (wall|tree) (on purpose)?)\b",

            # Future-tense planning ("tonight I'll", "tomorrow I'm going to")
            r"\b(tonight|this (evening|night)|tomorrow|later (today|tonight))\b.*\b(will|'ll|going to|gonna|plan|planning)\b.*\b(die|kill|end( it)?|hurt|harm|overdose|jump)\b",

            # Negation-style hopeless expressions (explicit)
            r"\b(no (reason|point|purpose) (to )?(live|continue)|nothing matters|nothing left|no way out)\b",

            # Implicit / emotional crisis phrases (hopelessness, burden)
            r"\b(hopeless|worthless|useless|a burden|better off dead|wish I (were|was) dead|tired of living|don'?t want to live|give up on life|done with life)\b",

            # Temporal immediacy (now/tonight/doing it now)
            r"\b(now|right now|doing it (now|tonight)|about to (do it|kill myself)|this minute|immediately)\b.*\b(die|kill|end|hurt|overdose|jump|hang)\b",

            # Emojis / short symbolic forms and misspellings (catch many compact signals)
            r"(💀|🔪|🔫|💊|🪢|i'?m done|im done|im finished|im finished with life|im going to die|im gonna die|gonna die)"
        ]
        
        # DONE: Define medical request patterns
        self.medical_keywords = [
            # Examples:
            # "diagnose", "what condition",
            # DONE: Add medical request indicators
            # --- Diagnosis requests ---
            "diagnose", "diagnosis", "self-diagnose", "self diagnosis",
            "what condition", "what disorder", "what illness", "what disease",
            "is this a disorder", "is this a condition", "is this an illness",
            "do I have", "could it be", "symptoms of", "signs of",
            "what's wrong with me", "check if I have", "test if I have",
            "professional diagnosis", "clinical opinion",

            # --- Medication queries ---
            "prescribe", "prescription", "can you prescribe", "give me medicine",
            "medication", "meds", "pills", "tablets", "antidepressant", "what pills"
            "antianxiety", "ssri", "dosage", "adjust dosage", "stop meds",
            "change medication", "refill prescription", "side effects",

            # --- Mental health specific ---
            "therapy plan", "treatment plan", "cure my depression", "cure my anxiety",
            "how to treat", "how to fix", "how to heal", "is it curable",
            "mental disorder", "psychiatric illness", "psychological evaluation",
            "life expectancy with", "is there a treatment",
            "am i depressed", "bipolar",
            "ocd", "ptsd", "adhd", "anxiety disorder", "panic disorder",
            "schizophrenia", "borderline personality disorder", "bpd",
            "dissociative identity disorder", "eating disorder",
            "substance abuse", "addiction", "alcoholism"
        ]
        
        # DONE: Medical patterns - regex for complex expressions
        self.medical_patterns = [
            # Example regex patterns:
            # r"\b(prescribe|recommend|suggest) (medication|pills|drugs)\b",
            # DONE: Add patterns for medical detection
            # --- Prescription requests ---
            r"\b(can you|please)?\s*(prescribe|recommend|suggest)\s+(medication|medicine|pills|drugs|antidepressants?|antianxiety|ssri)\b",
            r"\b(refill|change|adjust|stop)\s+(my\s+)?(meds?|medication|prescription|dosage)\b",
            r"\b(side effects?|effect of)\s+(this\s+)?(drug|medicine|medication|pill)\b",

            # --- Diagnostic questions ---
            r"\b(do I|could I|might I|am I)\s+(have|having|suffering from)\s+(.*)\b",
            r"\bis this (a|an)?\s*(disorder|condition|illness|disease)\b",
            r"\b(symptoms?|signs?) of (.*)\b",
            r"\bwhat('?s| is)\s*(wrong|happening)\s*(with me)?\b",

            # --- Treatment seeking ---
            r"\b(how (do I|to))\s*(treat|cure|heal|fix)\s+(.*)\b",
            r"\b(treatment|therapy)\s+(plan|options?|recommendations?)\b",
            r"\b(is there a|any)\s*(cure|treatment)\b",

            # --- Other medical/mental health boundary ---
            r"\b(psychological|psychiatric)\s+(evaluation|assessment|diagnosis)\b",
            r"\b(clinical|professional)\s+(opinion|diagnosis)\b",
            r"\blife expectancy (with|for)\s+(.*)\b"
        ]
        
        # DONE: Define harmful content patterns
        self.harmful_content = {
            "violence": [
                "kill", "murder", "stab", "shoot", "bomb", 
                "torture", "beat up", "attack", "blood", "slaughter",
                "assassinate", "execute", "lynch", "massacre",
                "terror", "revenge", "destroy", "ruin", "harm", 
                "hurt", "wound",
            ],  # DONE: Violence indicators
            "illegal": [
                "drug deal", "steal", "rob", "hack", "pirate",
                "bribe", "smuggle", "counterfeit", "fraud", "theft",
                "assault", "burglary", "embezzle", "sell drugs",
            ],   # DONE: Illegal activity indicators
            "harassment": [
                "bully", "harass", "threaten", "intimidate", "stalk",
                "dox", "insult", "mock", "taunt", "ridicule",
                "discriminate", "hate speech",
                "hate you", "worthless", "stupid", "idiot", "loser",
                "annoying", "kill yourself", "go die"
            ] # DONE: Harassment indicators
        }
        
        # TODO: Define confidence thresholds based on safety mode
        self.confidence_thresholds = {
            "strict": { 
                # Very sensitive → errs on the side of caution
                "crisis": 0.3,   # even weak matches are flagged
                "medical": 0.4,  # mild diagnostic/medication intent triggers boundary
                "harmful": 0.5   # moderate certainty required to avoid false positives
            },
            "balanced": { 
                # DONE: Adjust these
                # Balanced trade-off between sensitivity and user freedom
                "crisis": 0.45,   # need clearer signals of suicidal/self-harm ideation
                "medical": 0.6,  # allows symptom-sharing unless clear diagnosis request
                "harmful": 0.6   # ignores mild rude words, flags sustained patterns
            },
            "permissive": { 
                # DONE: Adjust these
                # Only block when highly confident → prioritizes free expression
                "crisis": 0.5,   # only strong suicidal/self-harm matches trigger
                "medical": 0.65, # user can discuss health; blocks only clear requests
                "harmful": 0.8   # allows edgy/hostile language unless very explicit
            }
        }
        
        # TODO: Define safety fallback templates
        # Copy complete templates from POLICY.md
        self.fallback_templates = {
            "crisis": """
I'm deeply concerned about what you're sharing. Your safety is my top priority, and I want you to know that help is available right now.

Please reach out to trained crisis counselors immediately:
- National Suicide Prevention Lifeline (U.S.): 988 (24/7)
- Crisis Text Line: Text HOME to 741741
- Samaritans of Singapore 24-hour Hotline: 1767
- Samaritans of Singapore 24-hour CareText: 9151-1767 (Whatsapp)
- Samaritans of Singapore Email: pat@sos.org.sg
- National Mindline 24-hour Helpline: 1771
- National Mindline 24-hour CareText: 6669-1771 (Whatsapp)
- Institute of Mental Health (IMH) Emergency Helpline: 6389-2222
- Singapore Association for Mental Health (SAMH) Crisis Helpline: 1800-283-7019
- National Anti-Violence Helpline: 1800-777-0000

You are not alone in this. It takes courage to talk about what you're going through, and reaching out for help is a strong and important step. While I cannot replace professional support, I can encourage you to connect with someone you trust, a close friend, family member, or a trained counselor, as soon as possible. If you are in immediate danger of harming yourself, please call emergency services right now. You deserve safety and care, and there are people ready to support you through this. 
            """,
            
            "medical": """
I understand you're looking for medical guidance, and I appreciate you reaching out. However, I'm not qualified to provide medical diagnoses or treatment recommendations.

It sounds like you may be worried about your health or experiencing distressing symptoms. 

For your health and safety, please consult with:
- A licensed psychiatrist for medication questions

What I can do here is help you reflect on your experiences, identify patterns in your mood or behavior, and prepare questions you may want to bring to your healthcare provider. I can also suggest general wellbeing strategies, such as stress management techniques, healthy routines, and communication tips that may help you until you receive professional care. Please remember: your health is important, and reaching out to a qualified professional is the safest way to get the support you need.
            """,

            "harmful": """
I cannot and will not provide assistance with that request as it could potentially cause harm.

This includes content related to violence, harassment, or illegal activities. My purpose is to be helpful and harmless, and I must refuse requests that promote or assist in any form of dangerous or unethical activity. It's important to keep this space safe and respectful for meaningful support.

If your message was not intended to promote harm, please feel free to rephrase so I can better understand your needs. I am here to help you with emotional reflection, safe coping strategies, and preparing for conversations with qualified professionals. 

If you are feeling strong emotions that come out as anger or frustration, I encourage you to express them in words that are safe and constructive. This will allow us to focus on what's troubling you and explore healthier ways forward. Thank you for respecting these boundaries, it helps ensure this system remains a safe place for support.

If you are experiencing thoughts of self-harm or harming others, please reach out to a crisis hotline or emergency services immediately. My core function is to support your well-being, and I am unable to engage in conversations that could lead to harm. Instead, I can provide resources for mental health support, offer emotional guidance, or discuss a different, safer topic.
            """,
            
            "disclaimer": """
Welcome to the Psychological Pre-Consultation Support System.

IMPORTANT DISCLAIMER:
This is an AI support system designed to provide initial emotional support and guidance. Please note:
- I am not a licensed clinician and cannot diagnose, prescribe, or treat medical or psychological conditions.  
- I cannot replace professional therapy, counseling, or medical care.  
- I cannot guarantee complete accuracy or appropriateness of responses.  
- I may not always fully understand your situation.  
- Conversations may be logged securely for system improvement, but they are not a substitute for confidential therapy.  

When to Seek Immediate Help:
- If you are in crisis or experiencing thoughts of self-harm
- If you have a medical emergency or urgent health concern

Crisis Resources: 
- Samaritans of Singapore 24-hour Hotline: 1767
- Samaritans of Singapore 24-hour CareText: 9151-1767 (Whatsapp)
- Samaritans of Singapore Email: pat@sos.org.sg
- National Mindline 24-hour Helpline: 1771
- National Mindline 24-hour CareText: 6669-1771 (Whatsapp)
- Institute of Mental Health (IMH) Emergency Helpline: 6389-2222
- Singapore Association for Mental Health (SAMH) Crisis Helpline: 1800-283-7019
- National Anti-Violence Helpline: 1800-777-0000

What I Can Offer:
- A listening, supportive conversation.  
- Help identifying emotions and patterns.
- Guidance on coping strategies and self-care.
- Preparation for seeking professional help.
- Encouragement to reach out to trusted individuals or professionals.
- General information about mental health topics.

Your wellbeing is important. How can I support you today?
            """,
        }
    
    def moderate(
        self,
        user_prompt: str,
        model_response: Optional[str] = None,
        context: Optional[List[Dict]] = None,
    ) -> ModerationResult:
        """
        Perform moderation on user input and/or model output.
        
        Args:
            user_prompt: The user's input text
            
        Returns:
            ModerationResult with action and explanation
            
        IMPLEMENTATION ORDER:
        1. Check crisis (highest priority - must not miss)
        2. Check medical (prevent harmful advice)
        3. Check harmful content (filter inappropriate)
        """
        
        # Example skeleton:
        # Step 1: Check for crisis indicators (highest priority)
        crisis_check = self._check_crisis(user_prompt)
        if crisis_check.action != ModerationAction.ALLOW:
            logger.warning(f"Crisis detected: {crisis_check.reason}")
            return crisis_check
        
        # TODO: Other Steps - Check for ???
        # Step 2: Check for medical requests
        medical_check = self._check_medical(user_prompt)
        if medical_check.action != ModerationAction.ALLOW:
            logger.info(f"Medical request detected: {medical_check.reason}")
            return medical_check
        
        # Step 3: Check for harmful content
        harmful_check = self._check_harmful(user_prompt)
        if harmful_check.action != ModerationAction.ALLOW:
            logger.info(f"Harmful content detected: {harmful_check.reason}")
            return harmful_check

        # If model response provided, check it
        if model_response:
            output_check = self._check_model_output(model_response)
            if output_check.action != ModerationAction.ALLOW:
                logger.warning(f"Output violation: {output_check.reason}")
                return output_check
        
        # Check context for concerning patterns
        if context:
            context_check = self._check_context_patterns(context)
            if context_check.action != ModerationAction.ALLOW:
                logger.info(f"Context concern: {context_check.reason}")
                return context_check
        
        # Default: Allow
        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="Content passes all safety checks",
            confidence=1.0,
        )
    
    def _check_crisis(self, text: str) -> ModerationResult:
        """
        Check for crisis indicators.
        
        DONE: Implement crisis detection
        
        ALGORITHM:
        1. Convert text to lowercase
        2. Check against crisis_keywords:
           - If found, set confidence = 0.7
           - Track which keywords were found
        3. Check against crisis_patterns:
           - If matched, set confidence = 0.8-0.9
           - Use re.search() for each pattern
        4. If multiple matches, use MAXIMUM confidence
        5. Get threshold for current safety_mode
        6. If confidence >= threshold:
           - Return BLOCK action
           - Include crisis fallback_response
           - Add descriptive tags
        7. Otherwise return ALLOW
        """

        text_lower = text.lower()
        detected_keywords = []
        confidence = 0.0

        # Keyword checking
        for keyword in self.crisis_keywords:
            if keyword in text_lower:
                detected_keywords.append(keyword)
                confidence = max(confidence, 0.7)

        # Pattern checking
        for pattern in self.crisis_patterns:
            if re.search(pattern, text_lower):
                detected_keywords.append(f"pattern:{pattern}")
                confidence = max(confidence, 0.85)
        
        # Maixmum confidence if multiple matches
        if len(detected_keywords) > 4:
            confidence = max(confidence, MAXIMUM_CONFIDENCE := 0.95)
        
        # Threshold comparison
        threshold = self.confidence_thresholds[self.safety_mode]["crisis"]

        if confidence >= threshold:
            return ModerationResult(
                action=ModerationAction.BLOCK,
                tags=["crisis"] + detected_keywords,
                reason=f"Crisis indicators detected with confidence {confidence:.2f}",
                confidence=confidence,
                fallback_response=self.fallback_templates["crisis"],
            )
        
        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="No crisis indicators detected",
            confidence=confidence,
        )
    
    def _check_medical(self, text: str) -> ModerationResult:
        """
        Check for medical requests.
        
        TODO: Implement medical request detection
        
        ALGORITHM:
        1. Convert text to lowercase
        2. Check against medical_keywords (confidence = 0.7)
        3. Check against medical_patterns (confidence = 0.85)
        4. Use maximum confidence if multiple matches
        5. Compare against threshold for safety_mode
        6. Return SAFE_FALLBACK if threshold exceeded
        
        Note: Use SAFE_FALLBACK, not BLOCK, for medical requests
        """
        text_lower = text.lower()
        detected_keywords = []
        confidence = 0.0

        # DONE: Implement keyword checking
        # Similar to crisis checking but with medical keywords
        for keyword in self.medical_keywords:
            if keyword in text_lower:
                detected_keywords.append(keyword)
                confidence = max(confidence, 0.7)
        
        # DONE: Implement pattern checking
        # Similar to crisis checking but with medical patterns
        for pattern in self.medical_patterns:
            if re.search(pattern, text_lower):
                detected_keywords.append(f"pattern:{pattern}")
                confidence = max(confidence, 0.85)
        
        # DONE: Threshold comparison and return
        # Remember to use ModerationAction.SAFE_FALLBACK for medical
        threshold = self.confidence_thresholds[self.safety_mode]["medical"]
        if confidence >= threshold:
            return ModerationResult(
                action=ModerationAction.SAFE_FALLBACK,
                tags=["medical"] + detected_keywords,
                reason=f"Medical request indicators detected with confidence {confidence:.2f}",
                confidence=confidence,
                fallback_response=self.fallback_templates["medical"],
            )
        
        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="No medical requests detected",
            confidence=confidence,
        )
    
    def _check_harmful(self, text: str) -> ModerationResult:
        """
        Check for harmful content.
        
        TODO: Implement harmful content detection
        
        ALGORITHM:
        1. Convert text to lowercase
        2. For each category in harmful_content:
           - Check if any keywords present
           - Track which categories triggered
        3. Set confidence = 0.75 for any match
        4. Compare against threshold
        5. Return BLOCK if threshold exceeded
        
        Include triggered categories in tags for debugging
        """

        text_lower = text.lower()
        detected_categories = []
        confidence = 0.0

        # Check keywords in each harmful category
        for category, keywords in self.harmful_content.items():
            for keyword in keywords:
                if keyword in text_lower:
                    detected_categories.append(category)
                    confidence = max(confidence, 0.75)
                    break  # No need to check more keywords in this category
            
        # Threshold comparison
        threshold = self.confidence_thresholds[self.safety_mode]["harmful"]
        if confidence >= threshold:
            return ModerationResult(
                action=ModerationAction.BLOCK,
                tags=detected_categories,
                reason=f"Harmful content detected in categories: {', '.join(detected_categories)} with confidence {confidence:.2f}",
                confidence=confidence,
                fallback_response=self.fallback_templates["harmful"],
            )
        
        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="No harmful content detected",
            confidence=confidence,
        )
    
    def _check_model_output(self, response: str) -> ModerationResult:
        """
        Check model output for policy violations.
        
        TODO: Ensure model didn't provide medical advice or break boundaries
        
        ALGORITHM:
        1. Check for medical_keywords that shouldn't appear
        2. Look for diagnosis-like statements
        3. Check for treatment recommendations
        4. Return SAFE_FALLBACK if violations found

        """

        response_lower = response.lower()
        violations = []

        # Check for medical keywords in output
        for keyword in self.medical_keywords:
            if keyword in response_lower:
                violations.append(f"medical:{keyword}")

        # Check for diagnostic statements
        diagnostic_patterns = [
            r"\b(you have|you are suffering from|diagnosed with|it is likely you have)\b",
            r"\b(this means you have|this indicates you have|you may have)\b"
        ]
        for pattern in diagnostic_patterns:
            if re.search(pattern, response_lower):
                violations.append(f"diagnosis_pattern:{pattern}")
        
        # Check for treatment recommendations
        treatment_patterns = [
            r"\b(you should|you need to|it is recommended to|you must)\b.*\b(take|use|start|stop|change)\b.*\b(medication|therapy|treatment|drugs?)\b",
            r"\b(the best treatment is|the best medication is)\b",
            r"\btry (ssri|prozac|xanax|antidepressants)\b"
        ]
        for pattern in treatment_patterns:
            if re.search(pattern, response_lower):
                violations.append(f"treatment_pattern:{pattern}")
        
        if violations:
            return ModerationResult(
                action=ModerationAction.SAFE_FALLBACK,
                tags=violations,
                reason=f"Model output contains medical advice or diagnosis: {', '.join(violations)}",
                confidence=0.9,
                fallback_response=self.fallback_templates["medical"],
            )
        
        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="Model output is appropriate",
            confidence=1.0,
        )
    
    def _check_context_patterns(self, context: List[Dict]) -> ModerationResult:
        
        # Check for escalation
        crisis_count = 0
        for turn in context:
            if turn.get("role") == "user":
                content = turn.get("content", "").lower()
                for keyword in self.crisis_keywords:
                    if keyword in content:
                        crisis_count += 1
        
        if crisis_count >= 3:
            return ModerationResult(
                action=ModerationAction.SAFE_FALLBACK,
                tags=["pattern_escalation", "repeated_crisis"],
                reason="Escalating crisis pattern detected",
                confidence=0.8,
                fallback_response=self.fallback_templates["crisis"],
            )
        
        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="Conversation pattern is safe",
            confidence=1.0,
        )
    
    def get_disclaimer(self) -> str:
        """Get initial disclaimer."""
        return self.fallback_templates.get("disclaimer", "")

# Singleton instance
_moderator_instance = None

def get_moderator() -> Moderator:
    """Get singleton moderator instance."""
    global _moderator_instance
    if _moderator_instance is None:
        _moderator_instance = Moderator()
    return _moderator_instance