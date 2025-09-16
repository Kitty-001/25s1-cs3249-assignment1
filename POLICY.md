# Safety and Moderation Policy

## Overview

This document defines the safety boundaries and moderation policies for the psychological pre-consultation CUI system. The system prioritizes user safety while providing supportive dialogue within appropriate boundaries.

## Policy Framework

### 1. Safety Categories

#### 1.1 Crisis Situations

**Definition**: Immediate risk of harm to self or others

**Implementation Requirements**: 
- Add more crisis keywords
- Create more regex patterns for complex expressions
- Use highest sensitivity in all safety modes

```python
# Student Implementation Required:
# Minimum 20 keywords covering various crisis expressions
CRISIS_KEYWORDS = [
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
    # DONE: Add comprehensive list
]

# Minimum 8 regex patterns for complex expressions
CRISIS_PATTERNS = [
    # Example patterns (add more regex patterns):
    r"\b(want|going|plan|ready) to (die|kill|hurt|end)\b",
    r"\b(thinking|thought) about (suicide|dying|ending it)\b",
    
    # Action / intent oriented (explicit)
    r"\b(want|wanna|wanna|wanna|wanna|wanna|wanting|planning|plan|going|gonna|ready)\s+(to|2)\s+(die|kill( myself)?|end( my life| it all)?|hurt( myself)?)\b",

    # Compact action forms and slang (kms, unalive)
    r"\b(kms|killme|kill myself|kill myself|unalive|off myself|offme|off myself|hurt myself|shot myself|shoot myself|shooting myself|hang myself)\b",
    r"\b(suicide|suicidal|suicid(al)?|su1cide|sucide|sui.cide)\b",

    # Specific methods / immediate danger indicators
    # Updated pattern for taking pills/medication
    r"\b(take|taking|took)\b\s+((too\s+)?many|(a\s+)?(lot|bunch|handful) of)\s+(pills|medication|tablets|tablets)\b"
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
    # DONE: Add more patterns to reach minimum 8
]
```

**Action**: `BLOCK` + Crisis referral

**Example Response Template**: 

```text
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
```

#### 1.2 Medical Requests

**Definition**: Requests for diagnosis, treatment, or medication advice

**Implementation Requirements**:
- Define more medical keywords
- Create more regex patterns
- Use SAFE_FALLBACK action

```python
# Student Implementation Required:
# Minimum 20 keywords
MEDICAL_INDICATORS = [
    # Diagnosis requests (add more keywords):
    "diagnose", "diagnosis", "self-diagnose", "self diagnosis",
    "what condition", "what disorder", "what illness", "what disease",
    "is this a disorder", "is this a condition", "is this an illness",
    "do I have", "could it be", "symptoms of", "signs of",
    "what's wrong with me", "check if I have", "test if I have",
    "professional diagnosis", "clinical opinion",
    
    # Medication/treatment (add more keywords):
    "prescribe", "prescription", "can you prescribe", "give me medicine",
    "medication", "meds", "pills", "tablets", "antidepressant", "what pills"
    "antianxiety", "ssri", "dosage", "adjust dosage", "stop meds",
    "change medication", "refill prescription", "side effects",
    
    # Mental health specific (add more keywords):
    "therapy plan", "treatment plan", "cure my depression", "cure my anxiety",
    "how to treat", "how to fix", "how to heal", "is it curable",
    "mental disorder", "psychiatric illness", "psychological evaluation",
    "life expectancy with", "is there a treatment",
    "am i depressed", "bipolar",
    "ocd", "ptsd", "adhd", "anxiety disorder", "panic disorder",
    "schizophrenia", "borderline personality disorder", "bpd",
    "dissociative identity disorder", "eating disorder",
    "substance abuse", "addiction", "alcoholism"
    # DONE: Add more keywords to reach minimum 20
]

# Minimum 8 regex patterns for complex expressions
MEDICAL_PATTERNS = [
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
    # DONE: Add more patterns to reach minimum 8
]
```

**Action**: `SAFE_FALLBACK`

**Response Template (Complete with structured format)**: 

```text
I understand you're looking for diagnosis or medical guidance, and I appreciate you reaching out. However, I'm not qualified to provide medical diagnoses or treatment recommendations.

It sounds like you may be worried about your health or experiencing distressing symptoms. 

For your health and safety, please consult with:
- A licensed psychiatrist for medication questions

What I can do here is help you reflect on your experiences, identify patterns in your mood or behavior, and prepare questions you may want to bring to your healthcare provider. I can also suggest general wellbeing strategies, such as stress management techniques, healthy routines, and communication tips that may help you until you receive professional care. Please remember: your health is important, and reaching out to a qualified professional is the safest way to get the support you need.
```

#### 1.3 Harmful Content

**Definition**: Violence, illegal activities, harassment

**Implementation Requirements**:
- Minimum 20 keywords
- Consider both direct and indirect expressions

```python
# Student Implementation Required:
HARMFUL_CATEGORIES = {
    "violence": [
        r"\b(kill|murder|assassinate|execute)\b.*\b(them|him|her|you|people|someone|anyone|every(one|body))\b",
        r"\b(shoot|stab|attack|bomb|hurt|harm)\b.*\b(you|him|her|them)\b",
        r"\b(torture|beat up|assault)\b",
        r"\b(terrorist|massacre|revenge|slaughter)\b",
        # DONE: Add more keywords
    ],
    
    "illegal": [
        r"\b(drug deal|steal|rob|hack|pirate|bribe|smuggle|counterfeit|fraud|theft|burglary|embezzle|sell drugs)\b",
        r"\b(make|buy|sell|use)\s+(illegal|unlicensed|fake|stolen)\s+(drugs|weapons|firearms|explosives|contraband)\b",
        r"\b(how to|ways to|methods to)\s+(commit|get away with|avoid getting caught for)\s+(a )?(crime|murder|theft|robbery|fraud|hacking|drug dealing)\b", 
        # DONE: Add more keywords
    ],
    
    "harassment": [
        r"\b(bully|harass|threaten|intimidate|stalk|dox|kill|hurt|stab)\b.*\b(you|him|her|them)\b",
        r"\b(hate|worthless|stupid|idiot|loser)\b.*\b(you|him|her|them)\b",
        r"\b(insult|mock|taunt|ridicule|discriminate|hate speech)\b",
        # DONE: Add more keywords
    ]
}
```

**Action**: `BLOCK`

**Example Response Template (Complete this with 150-200 words)**: 

```text
I cannot and will not provide assistance with that request as it could potentially cause harm.

This includes content related to violence, harassment, or illegal activities. My purpose is to be helpful and harmless, and I must refuse requests that promote or assist in any form of dangerous or unethical activity. It's important to keep this space safe and respectful for meaningful support.

If your message was not intended to promote harm, please feel free to rephrase so I can better understand your needs. I am here to help you with emotional reflection, safe coping strategies, and preparing for conversations with qualified professionals. 

If you are feeling strong emotions that come out as anger or frustration, I encourage you to express them in words that are safe and constructive. This will allow us to focus on what's troubling you and explore healthier ways forward. Thank you for respecting these boundaries, it helps ensure this system remains a safe place for support.

If you are experiencing thoughts of self-harm or harming others, please reach out to a crisis hotline or emergency services immediately. My core function is to support your well-being, and I am unable to engage in conversations that could lead to harm. Instead, I can provide resources for mental health support, offer emotional guidance, or discuss a different, safer topic.
```

#### 1.4 Supportive Dialogue

**Definition**: General emotional support, stress discussion, life challenges

**Acceptable Topics** (define at least 10):
```python
SUPPORTIVE_TOPICS = [
    "stress management",
    "relationship challenges",
    "work-life balance",
    "anxiety coping",
    "grief and loss",
    # TODO: Add at least 5 more acceptable topics
]
```

**Action**: `ALLOW`

### 2. Action Definitions

- **ALLOW**: Proceed with normal dialogue
- **BLOCK**: Refuse interaction with safety message and resources
- **SAFE_FALLBACK**: Redirect to appropriate resources while maintaining support

### 3. Confidence and Ambiguity

**Confidence Score Guidelines**:
- Keyword match: 0.7 confidence
- Pattern match: 0.8-0.9 confidence
- Multiple matches: Use maximum confidence

**Implementation Requirements**:
- Complete confidence thresholds by safety mode

**Confidence Thresholds by Safety Mode**:

```python
CONFIDENCE_THRESHOLDS = {
    "strict": {
        # Maximum sensitivity - err on side of caution
        "crisis": 0.3,   # Very low threshold for crisis detection
        "medical": 0.4,  # Low threshold for medical boundaries
        "harmful": 0.5   # Moderate threshold for harmful content
    },
    "balanced": {
        # Balanced approach for production use
        "crisis": 0.45,   # need clearer signals of suicidal/self-harm ideation
        "medical": 0.6,  # allows symptom-sharing unless clear diagnosis request
        "harmful": 0.6   # ignores mild rude words, flags sustained patterns
    },
    "permissive": {
        # Minimum filtering - only clear violations
         "crisis": 0.5,   # only strong suicidal/self-harm matches trigger
        "medical": 0.65, # user can discuss health; blocks only clear requests
        "harmful": 0.8   # allows edgy/hostile language unless very explicit
    }
}
```

### 5. Response Templates

**Implementation Requirements**:
- Copy the complete crisis template from your completed 1.1 Crisis Situations above.
- Copy the complete medical template from your completed 1.2 Medical Requests above.
- Copy the complete harmful template from your completed 1.3 Harmful Content above.
- Complete disclaimer template.

```python
RESPONSE_TEMPLATES = {
    "crisis": """
I'm deeply concerned about what you're sharing. Your safety is my top priority, and I want you to know that help is available right now.

Please reach out to trained crisis counselors immediately:
- Samaritans of Singapore 24-hour Hotline: 1767
- Samaritans of Singapore 24-hour CareText: 9151-1767 (Whatsapp)
- National Mindline 24-hour Helpline: 1771
- National Mindline 24-hour CareText: 6669-1771 (Whatsapp)
- Institute of Mental Health (IMH) Emergency Helpline: 6389-2222
- Singapore Association for Mental Health (SAMH) Crisis Helpline: 1800-283-7019
- National Anti-Violence Helpline: 1800-777-0000

You are not alone in this. It takes courage to talk about what you're going through, and reaching out for help is a strong and important step. Please call emergency services if you are in immediate danger. You deserve support, and there are people ready to help you through this difficult time. 
    """,
    
    "medical": """
I understand you're looking for medical guidance, and I appreciate you reaching out. However, I'm not qualified to provide medical diagnoses or treatment recommendations.

For your health and safety, please consult with:
- A licensed psychiatrist for medication questions

What I can do is:
- Help you reflect on your experiences and identify patterns in your mood or behavior.
- Prepare questions you may want to bring to a healthcare provider.
- Suggest general wellbeing strategies, such as stress management techniques or healthy routines.

Please remember that your health is important, and reaching out to a qualified professional is the safest way to get the support you need.
    """,

     "harmful": """
I cannot and will not provide assistance with that request as it could potentially cause harm.

This includes content related to violence, harassment, or illegal activities. My purpose is to be helpful and harmless, and I must refuse requests that promote or assist in any form of dangerous or unethical activity.

If your message was not intended to promote harm and you are feeling strong emotions that come out as anger or frustration, I encourage you to express them in words that are safe and constructive. I am here to help you with emotional reflection and safe coping strategies.

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
    """
}
```
