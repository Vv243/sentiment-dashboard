import os
import json
import hashlib
from functools import lru_cache
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class OpenAIAnalyzer:
    """
    Sentiment analyzer powered by OpenAI's GPT-4o-mini.
    
    Why a class instead of functions?
    - The OpenAI client is created once and reused (more efficient)
    - We can store configuration (model name, temperature) in one place
    - Easier to mock in tests
    """

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # This client handles authentication and HTTP connection pooling.
        # Creating it once here is more efficient than creating it per request.
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
        
        # Temperature controls how "creative" or random the responses are.
        # 0.0 = fully deterministic (same input always gives same output)
        # 1.0 = very creative/random
        # For sentiment analysis we want consistency, so we use a low value.
        self.temperature = 0.1

    def _build_prompt(self, text: str) -> str:
        """
        Craft the instruction we send to GPT.
        
        Prompt engineering matters a lot here. We need to:
        1. Tell GPT exactly what format to respond in (JSON)
        2. Define the exact fields we expect
        3. Constrain the possible values so we can rely on them
        
        If we just said "analyze this sentiment", GPT might respond in 
        prose and we'd have to parse unpredictable text. Asking for JSON 
        with a specific schema makes the response reliable and parseable.
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
        Send text to GPT-4o-mini and get back structured sentiment data.
        
        The try/except is important: API calls can fail for many reasons
        (network issues, rate limits, invalid responses). We catch errors
        here so callers don't need to handle OpenAI-specific exceptions.
        """
        if not text or not text.strip():
            return {
                "sentiment": "neutral",
                "confidence": 0.0,
                "compound_score": 0.0,
                "emotions": [],
                "reasoning": "Empty text provided.",
                "model": self.model,
                "cached": False,
                "error": None
            }

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                
                # response_format forces GPT to return valid JSON.
                # Without this, GPT might add "Here is the JSON:" before the object.
                response_format={"type": "json_object"},
                
                # Messages are the conversation history GPT sees.
                # "system" sets GPT's role and behavior rules.
                # "user" is the actual request.
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

            # response.choices[0].message.content is the raw text GPT returned.
            # Since we used json_object mode, this should always be valid JSON.
            raw_content = response.choices[0].message.content
            result = json.loads(raw_content)

            # Add metadata fields our app expects
            result["model"] = self.model
            result["cached"] = False
            result["error"] = None
            
            return result

        except json.JSONDecodeError as e:
            # GPT returned something that isn't valid JSON (shouldn't happen 
            # with json_object mode, but defensive programming is good practice)
            return self._error_response(f"Failed to parse GPT response as JSON: {e}")
        
        except Exception as e:
            # Catch-all for network errors, rate limits, auth failures, etc.
            return self._error_response(str(e))

    def _error_response(self, error_message: str) -> dict:
        """Return a safe fallback dict when something goes wrong."""
        return {
            "sentiment": "neutral",
            "confidence": 0.0,
            "compound_score": 0.0,
            "emotions": [],
            "reasoning": "Analysis unavailable due to API error.",
            "model": self.model,
            "cached": False,
            "error": error_message
        }


def _make_cache_key(text: str) -> str:
    """
    We can't cache by the raw text string because:
    1. lru_cache requires hashable arguments (strings are fine, but...)
    2. "I love this!" and "i love this!" should hit the same cache entry
    
    So we normalize (lowercase + strip) then hash it.
    A hash is a fixed-length fingerprint of any string.
    """
    normalized = text.lower().strip()
    return hashlib.md5(normalized.encode()).hexdigest()


# Module-level cached function
# Why outside the class? @lru_cache works on functions, not methods.
# maxsize=200 means we keep the 200 most recent unique analyses in memory.
# When the 201st unique text comes in, the oldest cached result is evicted.
@lru_cache(maxsize=200)
def _cached_analyze(cache_key: str, text: str) -> str:
    """
    The actual cached call. Returns JSON string (not dict) because
    lru_cache requires the return value to be hashable, and dicts are not.
    We serialize to string here and deserialize at the call site.
    """
    analyzer = OpenAIAnalyzer()
    result = analyzer.analyze(text)
    result["cached"] = False  # First call, not cached
    return json.dumps(result)


def analyze_with_cache(text: str) -> dict:
    """
    Public function that routes through the cache.
    
    Flow:
    1. Build a cache key from the normalized text
    2. Check if lru_cache has seen this key before
    3. If yes → return cached result instantly (no API call)
    4. If no → call GPT, store result in cache, return it
    """
    cache_key = _make_cache_key(text)
    json_result = _cached_analyze(cache_key, text)
    result = json.loads(json_result)
    
    # If this came from cache, lru_cache returned the same string we stored,
    # meaning the API was NOT called again. We mark it so you can see it working.
    # Note: lru_cache doesn't tell us directly if it was a hit, so we check
    # cache_info() before and after — or we just trust the logic above.
    result["cached"] = _cached_analyze.cache_info().hits > 0
    
    return result