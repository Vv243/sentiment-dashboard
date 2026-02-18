"""
analyzer_contract.py - The shared response contract for all sentiment analyzers.

Every analyzer (VADER, Hybrid, OpenAI) must return a dict matching this exact shape.
This ensures the API layer, database layer, and frontend never need to know which
model ran - they just handle one consistent structure.

ADDING A NEW ANALYZER?
1. Return a dict matching ANALYZER_RESPONSE_SCHEMA
2. Use build_error_response() for error cases
3. Use build_standard_response() as a helper to avoid mistakes
"""

from typing import Optional

# ============================================================
# THE CONTRACT
# Every analyzer.analyze() must return a dict matching this.
# ============================================================

ANALYZER_RESPONSE_SCHEMA = {
    "text": str,                # The original input text
    "sentiment": str,           # "positive" | "negative" | "neutral" | "harmful"
    "emoji": str,               # "😊" | "😞" | "😐" | "⚠️"
    "scores": {
        "positive": float,      # 0.0 to 1.0
        "negative": float,      # 0.0 to 1.0
        "neutral": float,       # 0.0 to 1.0
        "compound": float       # -1.0 to 1.0 (overall score)
    },
    "confidence": float,        # 0.0 to 1.0 (how confident is the model?)
    "model": str,               # "vader" | "hybrid" | "gpt-4o-mini"
    "emotions": list,           # [] for VADER/Hybrid, populated for GPT
    "reasoning": str,           # "" for VADER/Hybrid, explanation for GPT
    "cached": bool,             # True if result came from cache, False otherwise
    "error": None,              # None on success, error string on failure
}

# ============================================================
# VALID VALUES
# Use these constants instead of hardcoding strings
# ============================================================

VALID_SENTIMENTS = {"positive", "negative", "neutral", "harmful"}

SENTIMENT_EMOJI = {
    "positive": "😊",
    "negative": "😞",
    "neutral":  "😐",
    "harmful":  "⚠️",
}

MODEL_VADER  = "vader"
MODEL_HYBRID = "hybrid"
MODEL_GPT    = "gpt-4o-mini"

# ============================================================
# HELPER FUNCTIONS
# Use these to build responses - reduces copy-paste errors
# ============================================================

def sentiment_to_emoji(sentiment: str) -> str:
    """Convert sentiment string to emoji. Defaults to 😐 for unknown values."""
    return SENTIMENT_EMOJI.get(sentiment, "😐")


def derive_scores_from_compound(compound: float) -> dict:
    """
    Derive positive/negative/neutral score breakdown from a compound score.
    
    Used by OpenAI analyzer since GPT only returns a single compound score,
    not a three-way breakdown. The math matches what HybridAnalyzer already does.
    
    Args:
        compound: float between -1.0 and 1.0
        
    Returns:
        dict with positive, negative, neutral, compound keys
    """
    compound = max(-1.0, min(1.0, compound))  # clamp just in case

    if compound > 0:
        positive = 0.5 + (compound * 0.5)
        negative = 0.5 - (compound * 0.5)
    else:
        positive = 0.5 + (compound * 0.5)
        negative = 0.5 - (compound * 0.5)

    neutral = 1 - abs(compound)

    # Normalize so they sum to 1.0
    total = positive + negative + neutral
    return {
        "positive": round(positive / total, 3),
        "negative": round(negative / total, 3),
        "neutral":  round(neutral / total, 3),
        "compound": round(compound, 3),
    }


def build_standard_response(
    text: str,
    sentiment: str,
    scores: dict,
    confidence: float,
    model: str,
    emotions: list = None,
    reasoning: str = "",
    cached: bool = False,
    error: str = None,
) -> dict:
    """
    Build a contract-compliant response dict.
    
    Use this in your analyzers instead of building dicts by hand.
    Guarantees all required fields are present with correct types.
    """
    return {
        "text": text,
        "sentiment": sentiment,
        "emoji": sentiment_to_emoji(sentiment),
        "scores": scores,
        "confidence": round(float(confidence), 3),
        "model": model,
        "emotions": emotions if emotions is not None else [],
        "reasoning": reasoning or "",
        "cached": cached,
        "error": error,
    }


def build_error_response(
    text: str,
    model: str,
    error_message: str,
) -> dict:
    """
    Build a contract-compliant error response.
    
    Use this when an analyzer fails - ensures errors are also standard-shaped
    so the API layer never crashes trying to access a missing key.
    """
    return build_standard_response(
        text=text,
        sentiment="neutral",
        scores=derive_scores_from_compound(0.0),
        confidence=0.0,
        model=model,
        emotions=[],
        reasoning="Analysis unavailable due to error.",
        cached=False,
        error=error_message,
    )


def validate_response(response: dict) -> list:
    """
    Check a response dict against the contract. Returns list of violations.
    
    Use this in tests to verify your analyzers are compliant.
    
    Example:
        result = my_analyzer.analyze("test text")
        violations = validate_response(result)
        assert violations == [], f"Contract violations: {violations}"
    """
    violations = []
    required_keys = ["text", "sentiment", "emoji", "scores",
                     "confidence", "model", "emotions", "reasoning",
                     "cached", "error"]

    for key in required_keys:
        if key not in response:
            violations.append(f"Missing required key: '{key}'")

    if "scores" in response:
        required_score_keys = ["positive", "negative", "neutral", "compound"]
        for key in required_score_keys:
            if key not in response.get("scores", {}):
                violations.append(f"Missing required scores key: '{key}'")

    if "sentiment" in response:
        if response["sentiment"] not in VALID_SENTIMENTS:
            violations.append(
                f"Invalid sentiment '{response['sentiment']}'. "
                f"Must be one of: {VALID_SENTIMENTS}"
            )

    if "emotions" in response:
        if not isinstance(response["emotions"], list):
            violations.append("'emotions' must be a list")

    if "cached" in response:
        if not isinstance(response["cached"], bool):
            violations.append("'cached' must be a bool")

    return violations