import os
import json
import hashlib
from functools import lru_cache
from openai import OpenAI
from dotenv import load_dotenv
from app.services.analyzer_contract import (
    build_standard_response,
    build_error_response,
    derive_scores_from_compound,
    MODEL_GPT,
)

load_dotenv()


class OpenAIAnalyzer:
    """
    Sentiment analyzer powered by OpenAI's GPT-4o-mini.

    Why a class instead of functions?
    - The OpenAI client is created once and reused (more efficient)
    - We can store configuration (model name, temperature) in one place
    - Easier to mock in tests

    Response shape conforms to analyzer_contract.py.
    All analyzers return the same shape so the API layer
    never needs to know which model ran.
    """

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        # This client handles authentication and HTTP connection pooling.
        # Creating it once here is more efficient than creating it per request.
        self.client = OpenAI(api_key=api_key)
        self.model = MODEL_GPT  # "gpt-4o-mini" - imported from contract

        # Temperature controls randomness.
        # 0.1 = near-deterministic, good for consistent sentiment analysis.
        self.temperature = 0.1

    def _build_prompt(self, text: str) -> str:
        """
        Craft the instruction we send to GPT.

        Prompt engineering matters here. We need to:
        1. Tell GPT exactly what format to respond in (JSON)
        2. Define the exact fields we expect
        3. Constrain the possible values so we can rely on them
        """
        return f"""Analyze the sentiment of the following text and respond with ONLY a valid JSON object.

Text to analyze: "{text}"

Respond with this exact JSON structure:
{{
    "sentiment": "positive" | "negative" | "neutral",
    "confidence": <float between 0.0 and 1.0>,
    "compound_score": <float between -1.0 and 1.0, where -1 is most negative and 1 is most positive>,
    "emotions": [<list of detected emotions from: joy, sadness, anger, fear, surprise, disgust, trust, anticipation>],
    "reasoning": "<one or two sentences explaining why you classified it this way>"
}}

Important:
- Return ONLY the JSON object, no other text
- compound_score should reflect nuance (e.g. mild positive = 0.3, strong positive = 0.9)
- emotions list should only include emotions that are clearly present
- reasoning should mention specific words or phrases that influenced your decision"""

    def analyze(self, text: str) -> dict:
        """
        Send text to GPT-4o-mini and get back a contract-compliant response.

        The try/except is important: API calls can fail for many reasons
        (network issues, rate limits, invalid responses). We catch errors
        here so callers don't need to handle OpenAI-specific exceptions.
        """
        if not text or not text.strip():
            return build_standard_response(
                text=text or "",
                sentiment="neutral",
                scores=derive_scores_from_compound(0.0),
                confidence=0.0,
                model=self.model,
                emotions=[],
                reasoning="Empty text provided.",
            )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,

                # response_format forces GPT to return valid JSON.
                # Without this, GPT might add "Here is the JSON:" before the object.
                response_format={"type": "json_object"},

                messages=[
                    {
                        "role": "system",
                        "content": "You are a sentiment analysis expert. Always respond with valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": self._build_prompt(text)
                    }
                ]
            )

            raw_content = response.choices[0].message.content
            gpt_result = json.loads(raw_content)

            # GPT returns compound_score - map it to our standard scores shape
            compound = float(gpt_result.get("compound_score", 0.0))
            scores = derive_scores_from_compound(compound)

            # Handle "mixed" - GPT sometimes returns this despite the prompt.
            # Map it to "neutral" so we stay within VALID_SENTIMENTS.
            sentiment = gpt_result.get("sentiment", "neutral").lower()
            if sentiment not in {"positive", "negative", "neutral"}:
                sentiment = "neutral"

            return build_standard_response(
                text=text,
                sentiment=sentiment,
                scores=scores,
                confidence=float(gpt_result.get("confidence", 0.0)),
                model=self.model,
                emotions=gpt_result.get("emotions", []),
                reasoning=gpt_result.get("reasoning", ""),
                cached=False,
                error=None,
            )

        except json.JSONDecodeError as e:
            # GPT returned something that isn't valid JSON.
            # Shouldn't happen with json_object mode, but defensive programming.
            return build_error_response(text, self.model, f"JSON parse error: {e}")

        except Exception as e:
            # Catch-all for network errors, rate limits, auth failures, etc.
            return build_error_response(text, self.model, str(e))


# ============================================================
# CACHING LAYER
# Sits outside the class because @lru_cache works on functions,
# not methods. The class handles API calls; this handles caching.
# ============================================================

def _make_cache_key(text: str) -> str:
    """
    Normalize and hash the input text to use as a cache key.

    Why hash instead of using the raw string?
    - "I love this!" and "i love this!" should hit the same cache entry
    - A fixed-length hash is more memory-efficient than storing long strings
    """
    normalized = text.lower().strip()
    return hashlib.md5(normalized.encode()).hexdigest()


@lru_cache(maxsize=200)
def _cached_analyze(cache_key: str, text: str) -> str:
    """
    The actual cached call. Returns a JSON string because
    lru_cache requires hashable return values, and dicts are not hashable.
    We serialize here and deserialize at the call site.

    maxsize=200: keep the 200 most recent unique analyses in memory.
    When the 201st unique text comes in, the oldest entry is evicted.

    Limitation: this cache is in-memory and per-process. It resets on
    server restart and is not shared across multiple workers.
    Production upgrade path: replace with Redis for persistence + sharing.
    """
    analyzer = OpenAIAnalyzer()
    result = analyzer.analyze(text)
    return json.dumps(result)


def analyze_with_cache(text: str) -> dict:
    """
    Public entry point for OpenAI analysis with caching.

    Flow:
    1. Build a cache key from the normalized text
    2. Check if lru_cache has seen this key before
    3. Cache hit  → return stored result instantly (no API call, no cost)
    4. Cache miss → call GPT, store result, return it

    The 'cached' field in the response tells you which path was taken.
    """
    cache_key = _make_cache_key(text)

    # Record hits before the call so we can detect if this call was a hit
    hits_before = _cached_analyze.cache_info().hits
    json_result = _cached_analyze(cache_key, text)
    hits_after = _cached_analyze.cache_info().hits

    result = json.loads(json_result)

    # If hits increased, lru_cache served this from memory - no API call made
    result["cached"] = hits_after > hits_before

    return result